$(function() {


    // Submit job on submit
    $(document).on('submit', '#job-form', function(e){
        e.preventDefault();
        console.log("form submitted!");  // sanity check
        create_job();
    });

    // Delete job on click
    $(document).on('click', '.delete', function(e){
        e.preventDefault();
        console.log("DEL form submitted!");
        var el = $(this);

        var job_id =el.attr("id");
        var job_primary_key = job_id.split('-')[2];
        console.log(job_primary_key); // sanity check
        delete_job(job_primary_key);
    });

    // Finished job on click
    $(document).on('click', '.finished', function(e){
        e.preventDefault();
        console.log("Done form submitted!");
        var el = $(this);

        var job_done_id =el.attr("id");
        var job_done_key = job_done_id.split('-')[2];
        console.log(job_done_key);// sanity check
        done_job(job_done_key);
    });

    // Delete completed job on click
    $(document).on('click', '.delete-completed', function(e){
        e.preventDefault();
        console.log("Delete all completed form submitted!");
        delete_completed();
    });

    //show form for edit
     $(document).on('click', '.edit', function(e){
         e.preventDefault();
         var el = $(this);

         var id =el.attr("id");
         var key = id.split('-')[2];
         console.log(key);
         console.log("Edit form submitted!");
         $("#job-title-"+ key).hide();
         $('.this_block_is_hidden').hide();
         $("#title-input-"+ key).show();
    });

    //edit job
     $(document).on('submit', '.edit-title-form', function(e){
         e.preventDefault();
         var el = $(this);

         var id =el.attr("id");
         var key = id.split('-')[2];
         console.log(key);
         console.log("edit form submitted!");  // sanity check
         edit_job(key);
    });

    // AJAX for adding job
    function create_job() {
        console.log("create job is working!");// sanity check
        $.ajax({
            type : "POST", // http method
            url : "create_job/", // the endpoint
            data : { job_title : $('#job_title').val() }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                $('#job_title').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                $("#jobs").prepend("<li class = 'active' id = 'job-"+json.pk+"' status-job='s-active'><div onclick='openBlock(this);'><strong>"+json.title+"</strong></div><div class='this_block_is_hidden'><a  id='delete-job-"+json.pk+"' class='delete'>delete  </a><a id='edite-job-"+json.pk+"' class='edit'>  edit  </a><a  id='delete-job-"+json.pk+"' class='finished'>  change </a></div><hr>");
                $("#item_left").hide();
                $("#active_jobs").prepend(" <p id = 'item_left'>Items left : " + json.active+"</p>");

                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // AJAX for delete job
    function delete_job(job_primary_key){
        console.log("active job is working!");
        $.ajax({
            url : "delete_job/", // the endpoint
            type : "POST", // http method
            data : { job_pk : job_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
                $('#job-'+job_primary_key).hide(); // hide the post on success
                $("#item_left").hide();
                $("#active_jobs").prepend(" <p id = 'item_left'>Items left : " + json.active+"</p>");

                if ( json.done === 0)
                    $("#all_completed").hide();
                else{
                    $("#all_completed").hide();
                    $("#job-delete-complete").prepend(" <a  id='all_completed' class='delete-completed' >Delete completed : " +  json.done+"</a>");
                }
                console.log("post deletion successful");
            },

            error : function(xhr,errmsg,err) {
                // Show an error
                $('#results').html("<div class='alert-box alert radius' data-alert>"+
                    "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // AJAX for finished job
    function done_job(job_done_key){
        console.log("done job is working!");
        $.ajax({
            url : "done_job/", // the endpoint
            type : "POST", // http method
            data : { job_done_pk : job_done_key }, // data sent with the delete request
            success : function(json) {
                // hide the post

                $("#h-all-finished").hide();
                $("#all-finished").prepend("<h3 id='h-all-finished'>You has been finished already "+json.allFinishedJobs+" jobs</h3>");

                if ( json.done === 0)
                    $("#all_completed").hide();
                else{
                    $("#all_completed").hide();
                    $("#job-delete-complete").prepend(" <a  id='all_completed' class='delete-completed' >Delete completed : " +  json.done+"</a>");
                }

                $("#item_left").hide();
                $("#active_jobs").prepend(" <p id = 'item_left'>Items left : " + json.active+"</p>");

                if (json.isdone)
                    document.getElementById("job-"+job_done_key).className = 'done';
                else
                    document.getElementById("job-"+job_done_key).className = 'active';

                console.log(json);
                console.log("job finished successful");

            },

            error : function(xhr,errmsg,err) {
                // Show an error
                $('#results').html("<div class='alert-box alert radius' data-alert>"+
                    "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // AJAX for delete completed
    function delete_completed() {
        console.log("delete completed is working!");// sanity check
        $.ajax({
            type : "POST", // http method
            url : "delete_completed_job/", // the endpoint
            data : { confirm : "yes" }, // data sent with the post request
            // handle a successful response
            success : function(json) {

                for (var i = 0; i < json.id.length; i++) {
                    $("#job-"+json.id[i]).hide();
                }
                $("#all_completed").hide();

                console.log("success"); // another sanity check
                console.log(json)
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // AJAX for edit job
    function edit_job(key){
        console.log("edit job is working!");
        $.ajax({
            url : "edit_job/", // the endpoint
            type : "POST", // http method
            data : { job_edit_pk : key, job_title : $('#title-input-'+key).val() }, // data sent with the delete request

            success : function(json) {

                console.log($('.edit-title-form').val());
                // hide the post
                $("#job-title-"+ key).hide();

                $("#title-input-"+ key).hide();

                if (json.isdone)
                    document.getElementById("job-"+key).className = 'done';
                else
                    document.getElementById("job-"+key).className = 'active';
                $("#job-"+key).prepend(" <div onclick='openBlock(this);' id = 'job-title-"+json.id+"'><strong >"+json.title+"</strong></div>");


                console.log(json);
                console.log("job finished successful");

            },

            error : function(xhr,errmsg,err) {
                // Show an error
                $('#results').html("<div class='alert-box alert radius' data-alert>"+
                    "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };


// This function gets cookie with a given name
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

    /*
     The functions below will create a header with csrftoken
     */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});