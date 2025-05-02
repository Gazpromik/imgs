$(document).ready(function() {
    $("#log_reg").one('click', function() {
        $(this).animate({opacity: "0"}, 500);
        $(this).hide();
        $("#log").show();
        $("#reg").show();
        $("#log").animate({opacity: "1", left: "-=50px"}, 500);
        $("#reg").animate({opacity: "1", left: "+=50px"}, 500);
    });

    $("#reg").click(function() {
        $("#register").show();
        $("#register").animate({opacity: "1"}, 400);
    });
    $("#exit_reg").on('click', function() {
        $("#register").animate({opacity: "0"}, 400);
        $("#register").hide();  
    });

    $("#log").click(function() {
        $("#login").animate({opacity: "1"}, 400);
        $("#login").show();
    });

    $("#exit_log").on('click', function() {
        $("#login").animate({opacity: "0"}, 400);
        $("#login").hide();
    });

    $("#exit_add_picture").on('click', function() {
        $("#add_picture").animate({opacity: "0"}, 400);
        $("#add_picture").hide();
    });

    $(".generator_open").on('click', function() {
        $(".generate_pic").animate({opacity: "1"}, 400);
        $(".generate_pic").show();
    });
    $("#exit_generate").on('click', function() {
        $(".generate_pic").animate({opacity: "0"}, 400);
        $(".generate_pic").hide();
    });

    // Обработчик формы регистрации
    $('#reg_form').on('submit', function(event) {
        event.preventDefault(); // Предотвращаем отправку формы через браузер

        // Собираем данные из формы
        const formData = $(this).serialize();

        // Отправляем AJAX-запрос
        $.ajax({
            url: '/register',
            type: 'POST',        // Метод запроса
            data: formData,
            success: function(response) {
                if(response.status == 'nickname_is_exists') {
                    $("#error_reg").html("Имя пользователя занято")
                }
                else if(response.status == 'email_is_exists') {
                    $("#error_reg").html("Почта занята");
                }
                else if(response.status == 'passwords_not_match') {
                    $("#error_reg").html("Пароли не совпадают");
                }
                else if(response.status == 'success') {
                    $('#register').animate({opacity: "0"}, 200);
                    $('#register').hide();
                    $(".confirm_email").animate({opacity: "1"}, 400);
                    $(".confirm_email").show();
                }
                
            },
            error: function(xhr, status, error) {
                $("#result").html(`Ошибка: ${error}`);
            }
        });
    });

    $('#confirm_button').on('click', function(event) {
        user_code = $('#email_code').val();
        
        $.ajax({
            url: '/confirm_email',
            type: 'POST',        // Метод запроса
            data: {user_code: user_code},
            success: function(response) {
                if(response.status == 'wait_to_confirm') {
                    $('#error_confirm').html('Введите код в поле выше')
                }
                else if(response.status == 'incorrect_code') {
                    $('#error_confirm').html('Введите код в поле выше')
                }
                else if(response.status == 'success') {
                    $(".confirm_email").animate({opacity: "0"}, 400);
                    $(".confirm_email").hide();
                    $('.buttons_header').hide();
                    $('#nickname_header').show();
                    $('#user_img_header').show();
                    $('#nickname_header').text(response['nickname']);
                    $('#nickname_stats').text(response['nickname']);
                    $('#email_data').text(response['email']);
                }
            }
        });

    });

    // Обработчик формы входа
    $('#log_form').on('submit', function(event) {
        event.preventDefault(); // Предотвращаем отправку формы через браузер

        // Собираем данные из формы
        const formData = $(this).serialize();

        // Отправляем AJAX-запрос
        $.ajax({
            url: '/login',
            type: 'POST',        // Метод запроса
            data: formData,
            success: function(response) {
                console.log(response.status)
                if(response.status == 'no_input') {
                    $('#error_log').css({'opacity': "1"});
                    $('#error_log').text('Поля не заполнены!');
                } else if(response.status == 'no_info' || response.status == 'access_denied') {
                    $('#error_log').css({'opacity': "1"});
                    $('#error_log').text('Неверный логин или пароль!');
                } else {
                    $('#login').animate({opacity: "0"}, 200);
                    $('#login').hide();
                    $('.buttons_header').hide();
                    $('#nickname_header').show();
                    $('#user_img_header').show();
                    $('#nickname_header').text(response['nickname']);
                    $('#nickname_stats').text(response['nickname']);
                    $('#email_data').text(response['email']);
                };
            },
            error: function(xhr, status, error) {
                $("#result").html(`Ошибка: ${error}`);
            }
        });
    });

    $("#nickname_header").click(function() {
        $('.user_stats').slideDown(400, function() {

        });
    });

    $('#close_stats').click(function() {
        $('.user_stats').slideUp(400, function() {

        });
    });
    $('#open_add_picture').click(function() {
        $('.add_picture').animate({opacity: "1"}, 400);
        $('.add_picture').show()
    });
    function timer() {
        $.ajax({
            url: '/update',
            type: 'POST',        // Метод запроса
            success: function(response) {
                // console.log(response);
                response_lenght = response.length - 1
                // console.log(response_lenght)
                $('.pictures').empty();
                // $('.pictures').append('<img id="title_picture" src="/static/main_picture.jpg" alt="">')
                for (let i = 0; i <= response_lenght; i++) {
                    // console.log(i)
                    $('.pictures').append(`<img class="picture" id="${response[i][0]}" src="${response[i][1]}" alt="">`)
                    // $('.pictures').attr('src', response[i][1])
                }
            },
            error: function(xhr, status, error) {
                $("#result").html(`Ошибка: ${error}`);
            }
        });
    }
    setInterval(timer, 500)

    
    $('#get_form').on('submit', function(event) {
        event.preventDefault();
    
        let formData = new FormData(this);
    
        $.ajax({
            url: '/get_img',
            type: 'POST',        
            data: formData,
            contentType: false, 
            processData: false, 
            success: function(response) {
                if(response.error) {
                    $('#error_add').text(response.error);
                } else {
                    // $('.add_picture').animate({opacity: "0"}, 400);
                    // $('.add_picture').hide();
                }
            },
            error: function(xhr) {
                $("#error_add").text("Ошибка загрузки: " + xhr.responseText);
            }
        });
    });
    $('.pictures').on('click', '.picture', function() {
        url = $(this).attr('src');
        $.ajax({
            url: '/current_picture',
            type: 'GET',
            data: { url: url },
            success: function(data) {
                if(data.status == 'noUser') {
                    $(".warning").animate({opacity: "1"}, 400);
                    $(".warning").show();
                }
                else if(data.like == 'true') {
                    comments_lenght = data.comment.length - 1
                    $('#like_img').attr('src', '/static/like.png');
                    $('.current_picture').animate({ opacity: "1" }, 400);
                    $('.current_picture').show();
                    $('#huge_size').attr('src', data.img[0][1]);
                    $('#discribe_text').html(data.img[0][2]);
                    $('#count_likes').html(data.img[0][3]);
                    
                    $('.all_comments').empty();
                    for (let i = 0; i <= comments_lenght; i++) {
                        $('.all_comments').append(`<div class="comment">
                        <img id="comment_user" src="/static/user_image_1.png" alt="">
                        <p id="comment_nickname">${data.comment[i][3]}</p>
                        <p id="comment_date">${data.comment[i][4]}</p>
                    </div>
                    <div class="comment_text">
                        <p id="comment_text">${data.comment[i][2]}</p>
                    </div>`)
                    }
                }
                else {
                    comments_lenght = data.comment.length - 1
                    $('#like_img').attr('src', '/static/empty_like.png');
                    $('.current_picture').animate({ opacity: "1" }, 400);
                    $('.current_picture').show();
                    $('#huge_size').attr('src', data.img[0][1]);
                    $('#discribe_text').html(data.img[0][2]);
                    $('#count_likes').html(data.img[0][3]);

                    $('.all_comments').empty();
                    for (let i = 0; i <= comments_lenght; i++) {
                        $('.all_comments').append(`<div class="comment">
                        <img id="comment_user" src="/static/user_image_1.png" alt="">
                        <p id="comment_nickname">${data.comment[i][3]}</p>
                        <p id="comment_date">${data.comment[i][4]}</p>
                    </div>
                    <div class="comment_text">
                        <p id="comment_text">${data.comment[i][2]}</p>
                    </div>`)
                    }
                }
                
                
            },
            error: function(xhr, status, error) {
                console.error("Ошибка:", error);
            }
        });
       

        
    });
    $('#close_main_picture').click(function() {
        $('.current_picture').animate({opacity: "0"}, 400);
        $('.current_picture').hide();
    });
    $('.like').on('click', function() {
        img_src = $('#huge_size').attr('src');
        like_src = $('#like_img').attr('src');
        increace = 0;
        if(like_src == '/static/empty_like.png') {
            increace = 1
        }
        if(like_src == '/static/like.png') {
            increace = -1
        }
        // console.log(increace);
        // console.log(img_src);
        formData = {
            "src": img_src,
            "increace": increace
        }
        $.ajax({
            url: '/like',
            type: 'GET',
            data: formData,
            success: function(response) {
                if(response['img'] == 'noUser') {
                    $(".warning").animate({opacity: "1"}, 400);
                    $(".warning").show();
                }
                if(increace == 1) {
                    like = '/static/like.png';
                    $('#like_img').attr('src', like);
                    $('#count_likes').html(response["img"][3])
                }
                if(increace == -1) {
                    unlike = '/static/empty_like.png';
                    $('#like_img').attr('src', unlike);
                    $('#count_likes').html(response["img"][3])
                }
                
                
            },
            error: function(xhr, status, error) {
                console.error("Ошибка:", error);
            }
        });
        
        
    });
    $('#exit_from_acc').on('click', function() {
        $.ajax({
            url: '/exit_from_acc',
            type: 'GET',
            success: function(data) {
                $('.buttons_header').show();
                $('#nickname_header').hide();
                $('#user_img_header').hide();
                $('.user_stats').slideUp(400, function() {});
            }
        });
    });
    $('#exit_warning').on('click', function() {
        $(".warning").animate({opacity: "0"}, 400);
        $(".current_picture").animate({opacity: "0"}, 400);
        $(".warning").hide();
        $(".current_picture").hide();
    });
    $('#paste_comment').on('click', function() {
        src = $('#huge_size').attr('src');
        console.log(src);
        koment = $('#comment_input').val();
        $.ajax({
            url: '/comments',
            type: 'POST',
            data: {src: src, koment: koment},
            success: function(response) {
                $('.all_comments').append(`<div class="comment">
                    <img id="comment_user" src="/static/user_image_1.png" alt="">
                    <p id="comment_nickname">${response.comment[1]}</p>
                    <p id="comment_date">${response.comment[2]}</p>
                </div>
                <div class="comment_text">
                    <p id="comment_text">${response.comment[0]}</p>
                </div>`)
            }
        });
    });

    $('#generate_img_button').on('click', function() {
        discribe = $("#generate_input").val();
        $("#generating").show();
        $("#commit_img_button").hide();
        $("#successful_generate").hide();
        $.ajax ({
            url: '/generate_img',
            type: 'POST',
            data: {discribe: discribe},
            success: function(response) {
                $("#generating").hide();
                $("#commit_img_button").animate({opacity: "1"}, 400);
                $("#commit_img_button").show();
                $("#generate_img").attr('src', "data:image/png;base64," + response.img);
                $('#generate_img').show();
                $('#generate_notice').hide();
            }
        });
    });
    $('#commit_img_button').on('click', function() {
        $.ajax ({
            url: '/publish_img',
            type: 'POST',
            success: function(response) {
                $("#commit_img_button").animate({opacity: "0"}, 400);
                $("#commit_img_button").hide();
                $("#successful_generate").show();
            }
        });
    });

    $('#exit_confirm').on('click', function() {
        $.ajax ({
            url: '/exit_from_acc',
            type: 'GET',
            success: function(response) {
                $(".confirm_email").animate({opacity: "0"}, 400);
                $(".confirm_email").hide();
            }
        });
    });
});
