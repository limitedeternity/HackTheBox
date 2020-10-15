import argparse
import os
import shutil
import tempfile
from zipfile import ZipInfo, ZipFile

parser = argparse.ArgumentParser(description="Unzips a password protected .zip by performing a brute-force attack "
                                             "using either a word list, password list or a dictionary.",
                                 usage="BruteZIP.py -z zip.zip -d dict.txt")
parser.add_argument("-z", "--zip", metavar="", required=True, help="Path to the .zip file.")
parser.add_argument("-d", "--dict", metavar="", required=True, help="Path to the dictionary")
args = parser.parse_args()


class Zipped(ZipFile):
    def _extract_member(self, member, targetpath, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        arcname = member.filename.replace('/', os.path.sep)

        if os.path.altsep:
            arcname = arcname.replace(os.path.altsep, os.path.sep)

        arcname = os.path.splitdrive(arcname)[1]
        invalid_path_parts = ('', os.path.curdir, os.path.pardir)
        arcname = os.path.sep.join(x for x in arcname.split(os.path.sep)
                                   if x not in invalid_path_parts)
        if os.path.sep == '\\':
            arcname = self._sanitize_windows_name(arcname, os.path.sep)

        targetpath = os.path.join(targetpath, arcname)
        targetpath = os.path.normpath(targetpath)

        upperdirs = os.path.dirname(targetpath)
        if upperdirs and not os.path.exists(upperdirs):
            os.makedirs(upperdirs)

        if member.is_dir():
            if not os.path.isdir(targetpath):
                os.mkdir(targetpath)
            return targetpath

        with self.open(member, pwd=pwd) as source:
            if pwd:
                dirname = os.path.dirname(targetpath)
                basename = os.path.basename(targetpath)
                idx = basename.rfind(".")
                if idx != -1:
                    prefix, suffix = basename[:idx], basename[idx:]
                else:
                    prefix, suffix = basename, ""

                fid, tmptargetpath = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dirname)
                with open(fid, "wb") as target:
                    try:
                        shutil.copyfileobj(source, target)
                    except:
                        target.close()
                        os.unlink(tmptargetpath)
                        raise

                shutil.move(tmptargetpath, targetpath)

            else:
                with open(targetpath, "wb") as target:
                    shutil.copyfileobj(source, target)

        return targetpath


def extract_zip(zipf, password):
    try:
        zip_file = Zipped(zipf)
        zip_file.setpassword(password)
        zip_file.extractall()
        print(f"[+] Password for the .zip: {password.decode('utf-8')}")
        return True

    except:
        return False


def main(zipf, dictionary):
    if zipf == None or dictionary == None:
        print(parser.usage)
        return

    with open(dictionary, "rb") as txt_file:
        for password in map(lambda l: l.strip(), txt_file):
            if extract_zip(zipf, password):
                break


if __name__ == "__main__":
    main(args.zip, args.dict)
