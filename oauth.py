from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )
    def get_token(self,code):
        from urllib.parse import urlparse
        from urllib.request import urlopen
        link="https://graph.facebook.com/oauth/access_token?" "client_id="+self.consumer_id+"&redirect_uri="+self.get_callback_url()+"&client_secret="+self.consumer_secret+"&code="+code
        link= urlparse(link).geturl()
        response=urlopen(link).read()
        # return response.index('&')
        start= len("access_token=")
        end=len("&expires=5128227")

        response= response[start:]
        response=response[:-end]
        return response
      
    def get_exended_token(self,access_token):
        import facebook
        graph= facebook.GraphAPI(access_token)
        extended_token= graph.extend_access_token(self.consumer_id,self.consumer_secret)
        return extended_token

    def callback(self):
        if 'code' not in request.args:
            return None, None, 
        code= request.args['code']
        token= self.get_token(code)
        # return token
        from urllib.parse import urlparse
        link = "https://graph.facebook.com/me?access_token="+str(token)
        link =urlparse(link).geturl()
        # return link
        return "<a href="+link+"> Test Token </a>"
        # oauth_session = self.service.get_auth_session(
        #     data={'code': request.args['code'],
        #           'grant_type': 'authorization_code',
        #           'redirect_uri': self.get_callback_url()}
        # )
        
        # return (
        #     'facebook$' + me['id'],
        #     me.get('email').split('@')[0],  # Facebook does not provide
        #                                     # username, so the email's user
        #                                     # is used instead
        #     me.get('email'),
            
            
        # )


class TwitterSignIn(OAuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        me = oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        return social_id, username, None   # Twitter does not provide email
