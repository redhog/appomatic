function callWithProgress(url, data, description) {
  console.log(["callWithProgress", url, data, description]);

  $('body').append('<div class="modal"></div><div class="popup"><h1>' + description + ': <span class="status"></span></h1> <div class="progress"><div class="progress_meter" style="width: 0;"></div></div> <div class="output"></div></div>');
  $('body .popup').data('next', undefined);

  var update = function() {
    jQuery.ajax({
      dataType: 'json',
      url: "/admin/appomatic_appadmin/application/progress/" +  $('body .popup').data('pid'),
      success: function (data) {
	var last = data[data.length-1];
        console.log(last);
	$('body .popup .progress_meter').css('width', (100 * last.done) + "%");
	$('body .popup .status').html(last.status);
	$('body .popup .output').html(data.map(function(d) { return "<div>"+d.status+"</div>"; }).join(""));
	$('body .popup .output')[0].scrollTop = $('body .popup .output')[0].scrollHeight;

	var cont = function () {
	  if (last.next != undefined && last.next != $('body .popup').data('next')) {
	    $('body .popup').data('next', last.next);
 	    load(last.next);
	  } if (last.done < 1) {
	    update();
	  } else {
	    done();
	  }
        }
	setTimeout(cont, last.delay || 1000);
      },
      error: function (data) {
  	setTimeout(update, 1000);
      }
    });
  }
  var done = function () {
    $('body .modal').remove();
    $('body .popup').remove();
    window.location.reload();
  }
  var load = function (url, data) {
    console.log(["callWithProgressPart", url, data]);

    var load = function () {
      jQuery.ajax({
	dataType: 'json',
	url:url,
	data:data,
	success: function (data) {
	  console.log(["callWithProgressPartId", data.pid]);
	  $('body .popup').data('pid', data.pid);
	  update();
	},
	error: function (data) {
	  setTimeout(load, 1000);
	}
      });
    }
    load();
  }
  load(url, data);
}

function submitFormWithProgress(form, description) {
  if (form == undefined)
    form = jQuery("form");
  if (description == undefined)
    description = form.find("[name=action] [value=" + form.find("[name=action]")[0].value + "]").html();
  callWithProgress(form.attr("action"), form.serializeArray(), description);
}