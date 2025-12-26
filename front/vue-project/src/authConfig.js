export const msalConfig = {
    auth: {
    clientId: "989fb1e4-afa5-4d39-af9b-5345307ed12d",
    authority: `https://login.microsoftonline.com/9f119962-8c62-431c-a8ef-e7e0a42d11fc`,
    redirectUri: "http://localhost:8080/",
    },
    cache: {
        cacheLocation: "sessionStorage",
        storeAuthStateInCookie: false,
    }
};

export const loginRequest = {
    scopes: ["User.Read"]
};