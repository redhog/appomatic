function callWithProgress(url, data, description) {
 console.log(["callWithProgress", url, data, description]);

  $('body').append('<div class="modal"></div><div class="popup"><h1>' + description + ': <span class="status"></span></h1> <div class="progress"><div class="progress_meter" style="width: 0;"></div></div> <div class="output"></div></div>');

  var update = function() {
    jQuery.ajax({
      dataType: 'json',
      url: "/admin/appomatic_appadmin/application/progress/" +  $('body .popup').data('pid'),
      success: function (data) {
	var last = data[data.length-1];
	$('body .popup .progress_meter').css('width', last.percent_done + "%");
	$('body .popup .status').html(last.status);
	$('body .popup .output').html(data.map(function(d) { return "<div>"+d.status+"</div>"; }).join(""));
	if (last.percent_done != 100) {
  	  setTimeout(update, 1000);
        } else {
  	  setTimeout(done, 1000);
        }
      },
      error: function (data) {
  	setTimeout(update, 2000);
      }
    });
  }
  var done = function () {
    $('body .modal').remove();
    $('body .popup').remove();
    window.location.reload();
  }
  jQuery.ajax({
    dataType: 'json',
    url:url,
    data:data,
    success: function (data) {
      $('body .popup').data('pid', data.pid);
      update();
    }
  });
}

function submitFormWithProgress(form, description) {
  if (form == undefined)
    form = jQuery("form");
  if (description == undefined)
    description = form.find("[name=action] [value=" + form.find("[name=action]")[0].value + "]").html();
  callWithProgress(form.attr("action"), form.serializeArray(), description);
}