from django import forms
from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html
from django.utils.translation import gettext as _


class UserInfoForm(forms.Form):

    phone_number = forms.CharField(max_length=20)



class MyPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self, *args, **kwargs):
        fields_html = "".join(str(field) for field in self)

        return format_html(
            """<form action="{0}" method="post">
                    {1}
                    <div class="d-grid gap-2 my-3">
                        <button class="btn btn-primary" type="submit">
                            <i class="lni lni-paypal-original"></i> {2}
                        </button>
                    </div>
                </form>""",
            self.get_login_url(),
            format_html(fields_html),
            _('Pay Now'),
        )