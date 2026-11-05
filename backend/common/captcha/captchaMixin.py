from .captcha import CaptchaRunner

class CaptchaMixin:

    captcha_scope = None

    def initial(self, request, *args, **kwargs):

        super().initial(
            request,
            *args,
            **kwargs,
        )

        if self.captcha_scope:
            CaptchaRunner(
                request=request,
                scope=self.captcha_scope,
            ).run()