function updatePosts() {
    var d = $("#display");
    var last_modified = d.data("last_modified");
    console.log(last_modified);
    $.get("/grumblr/get-posts/" + last_modified)
        .done(function (data) {
            update(data);
        }).catch((a, b, c) => {
        console.log('err', a, b, c)
    });
}


function populateList() {
    $.get("/grumblr/get-posts")
        .done(function (data) {
            var d = $("#display");
            d.data('last_modified', data['last_modified']);
            console.log("populate max time " + d.data("last_modified"));
        });
}

function update(data) {
    var d = $("#display");
    d.data('last_modified', data['last_modified']);

    for (var i = 0; i < data.posts.length; i++) {
        var post = data.posts[i];

        var new_post = $("<span></span>");
        var $Div1 = $("<div></div>");

        var $div11 = $("<div class='left'></div>");

        $div11.append("<img class=\"profile\" src=" + post['profile_url'] + " alt=\"pofile photo\">");

        var $div12 = $("<div class='left'></div>");
        $div12.append('<a class=\"share\" href=' + static_profile_url + post.user_id + '>' + post['user_name'] + '</a><br>',
            '<x-small>' + post['time'] + '</x-small></div></div>');

        $Div1.append($div11, $div12, "<br><br>");

        var $Div2 = $("<div></div>");

        var $div21 = $("<div></div>");

        $div21.append($("<p></p>").html(post['content']));

        var $div22 = $("<div></div>");

        var btn = $("<a class=\"share waves-effect waves-teal btn-flat\" id=" + post['id'] + "><i class=\"material-icons share\">comment</i>Comment</a>");
        $div22.append(btn);

        //for diaplay comments
        var $div23 = $("<div class='col s12 solid'></div>");
        var comment_area_id = 'div-post-' + post.id;
        $div23.attr('id', comment_area_id);


        for (var j = 0; j < post.comments.length; j++) {
            var comment = post.comments[j];
            updateComment(comment);
        }


        $Div2.append($div21, $div22, $div23);

        new_post.append($Div1, $Div2, "<br><br><hr>");

        d.prepend(new_post);
    }
}

function updateComment(data) {
    var comment_area_id = '#div-post-' + data['post_id'];
    console.log(comment_area_id);
    var $div23 = $(comment_area_id);
    $div23.append("<hr>");
    var new_comment = $("<span></span>");
    var $c_Div1 = $("<div></div>");
    var $c_div11 = $("<div class='left'></div>");
    $c_div11.append("<img class=\"profile\" src=" + data['profile_url'] + " alt=\"pofile photo\">");
    var $c_div12 = $("<div class='left'></div>");
    $c_div12.append('<a class=\"share\" href=' + static_profile_url + data['user_id'] + '>' + data['user_name'] + '</a><br>',
        '<x-small>' + data['time'] + '</x-small></div></div>');

    $c_Div1.append($c_div11, $c_div12, "<br><br>");

    var $c_Div2 = $("<div></div>").append($("<p></p>").html(data['content']));
    new_comment.append($c_Div1, $c_Div2);

    $div23.append(new_comment);

}

var lastClick = 0;
$(document).ready(function () {
    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    // setup
    populateList();

    setInterval(updatePosts, 5000);

    $("#moment_form").trigger("reset");
    $("#comment_form").trigger("reset");

    $("#moment_form").on('submit', function (event) {
        event.preventDefault(); // Prevent form from being submitted

        var post = {};
        console.log("add-post");
        var inputs = $("#moment_form").serializeArray();

        $.each(inputs, function (i, input) {
            post[input.name] = input.value;
        });
        console.log(post);
        $.post('/grumblr/add-post', post).done(function (data) {
            update(data);
        });
        $("#moment_form").trigger("reset");
    });

    $("#display").on('click', ".share.waves-effect.waves-teal.btn-flat", function () {
        console.log(this.id);

        var id = this.id;
        if ($("#comment_form").is(":visible") && (lastClick != id)) {
            $("#comment_form").toggle();
        }

        lastClick = id;
        // append the form to that post
        var div_id = '#div-post-' + id;
        console.log(div_id);
        $(div_id).prepend($("#comment_form"));
        $("#comment_form").toggle();
    });

    $("#comment_form").on('submit', function (event) {
        event.preventDefault(); // Prevent form from being submitted
        var comment = {};
        var inputs = $("#comment_form").serializeArray();
        $.each(inputs, function (i, input) {
            comment[input.name] = input.value;
        });


        // get the id of the post
        var tmp = $("#comment_form").parent().attr('id');
        var post_id = tmp.substr(9);

        comment['post_id'] = parseInt(post_id);

        $.post('/grumblr/add-comment', comment).done(function (data) {
            console.log('comment', comment);
            updateComment(data);

        }).catch((a, b, c) => {
            console.log('comment err', a, b, c)
        });
        $("#comment_form").trigger("reset");
    });


});
