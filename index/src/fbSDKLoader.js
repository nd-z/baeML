class FbSDK { 
    
    static loadFbSDK() {
        window.fbAsyncInit = function() {
               window.FB.init({
                appId            : '1992517710981460',
                autoLogAppEvents : true,
                xfbml            : true,
                cookie           : true,
                version          : 'v2.9'
              });
              window.FB.AppEvents.logPageView();
            };

            (function(d, s, id) {
              var js, fjs = d.getElementsByTagName(s)[0];
              if (d.getElementById(id)) return;
              js = d.createElement(s); js.id = id;
              js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9&appId=1992517710981460";
              fjs.parentNode.insertBefore(js, fjs);
            }(document, 'script', 'facebook-jssdk'));
            return window.FB;
    }
}

export default FbSDK;