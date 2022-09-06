function login() {
    username = '';
    password = '';
    return {
        login_check() {
            console.log('dede');
            if (username && password) {
                $.ajax({
                    type: "POST",
                    url: "login",
                    data: JSON.stringify({'username': username, 'password': password}),
                    contentType: "application/json;charset=UTF-8",
                    dataType: "json",
                    success: function (result) {
                        if (result[0] === 'ok') {
                            window.location.href = 'index'
                        } else {
                            alert(result[1])
                        }
                    },
                });
            } else {
                alert("请输入所有信息!");
            }
        }
    }
}
