function switch-psuser {
    
    Param(
        [Parameter(Position=0)]
        [ValidateSet("john")]
        $User = "john"
    )

    switch($User)
    {
        "john"   { $username = "ARCHETYPE\john" ; $pw = "Password123!"}
    }

    $password = $pw | ConvertTo-SecureString -AsPlainText -Force
    $cred = New-Object System.Management.Automation.PSCredential -ArgumentList $username,$password
    New-PSSession -Credential $cred | Enter-PSSession
}
