


function registerUser() {
    console.log("here");

    var username = document.getElementById('username').value
    let passWordelement = document.getElementById('password')
    let confirmPasselement = document.getElementById('confirm-password')

    if (passWordelement.value !== confirmPasselement.value) {
        alert("Passwords don't match")
        return
    } else {
        password = passWordelement.value
    }



    var poolData = {
        UserPoolId: _config.cognito.userPoolId,
        ClientId: _config.cognito.clientId
    }

    // console.log(poolData);

    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);


    console.log(userPool);

    var attributeList = [];

    var dataEmail = {
        Name: 'email',
        Value: username,
    };


    var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);

    attributeList.push(attributeEmail)

    userPool.signUp(username, password, attributeList, null, function (
        err,
        result
    ) {
        if (err) {
            alert(err.message || JSON.stringify(err));
            return;
        }
        var cognitoUser = result.user;
        console.log('user name is ' + cognitoUser.getUsername());
        alert("Check your email for verification link")
    });

}
