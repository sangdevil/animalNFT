from django import forms
from gallery.models import Nft_object


class NFT_form(forms.ModelForm):
    class Meta:
        model = Nft_object  # 사용할 모델
        fields = ["title", "category","nft_image"]  # QuestionForm에서 사용할 Question 모델의 속성