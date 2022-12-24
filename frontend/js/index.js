

function login() {

    var authenticationData = {
        Username: document.getElementById('username').value,
        Password: document.getElementById('password').value
    };

    console.log(authenticationData);

    var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(
        authenticationData
    );
    var poolData = {
        UserPoolId: _config.cognito.userPoolId,
        ClientId: _config.cognito.clientId
    }


    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

    var userData = {
        Username: document.getElementById('username').value,
        Pool: userPool
    }

    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData)

    let redirect = false
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function (result) {
            var accessToken = result.getAccessToken().getJwtToken();
            console.log(accessToken);
            redirect = true

            if (redirect === true) {
                console.log("Redirecting ");
                return window.location.href = "./code.html"
            }
        },
        onFailure: function (err) {
            alert(err.message || JSON.stringify(err));
        }
    });



}