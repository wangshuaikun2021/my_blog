$(function () {
    function bindCaptchaBtnClick() {
        $("#captcha-btn").click(function (event) {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert("请输入邮箱");
                return;
            }
            $this.off("click");

            $.ajax("/myauth/captcha?email=" + email, {
                method: "GET",
                success: function (result) {
                    if (result["code"] === 200) {
                        alert("验证码已发送到您的邮箱，请注意查收");
                    }else{
                        alert(result["msg"]);
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
            let count_down = 6;
            let timer = setInterval(function () {
                if (count_down <= 0) {
                    $this.text("获取验证码");
                    clearInterval(timer);
                    bindCaptchaBtnClick();
                } else {
                    $this.text(count_down + "s");
                    count_down--;
                }
            }, 1000);
        })
    }
    bindCaptchaBtnClick();

});