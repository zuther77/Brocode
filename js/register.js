import {
    CognitoUserPool,
    CognitoUserAttribute,
    CognitoUser,
} from '..node_modules/';


function registerUser() {
    console.log("here");

    let userEmail = document.getElementById('username').value
    let passWord = document.getElementById('password')
    let confirmPass = document.getElementById('confirm-password')

    if (passWord.value !== confirmPass.value) {
        password = ''
        confirmPass = ''
        alert("Passwords don't match")
    } else {
        password = passWord.value
    }



    var poolData = {
        UserPoolId: _config.cognito.userPoolId,
        ClientId: _config.cognito.clientId
    }



    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
}