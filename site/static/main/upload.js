
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
	var cookies = document.cookie.split(';');
	for (var i = 0; i < cookies.length; i++) {
	    var cookie = jQuery.trim(cookies[i]);
	    // Does this cookie string begin with the name we want?
	    if (cookie.substring(0, name.length + 1) === (name + '=')) {
		cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		break;
	    }
	}
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$("#file-input").fileinput({
    theme: 'explorer-fas',
    // showPreview: false, 
    uploadUrl: 'main/upload',
    maxFileSize: 2048,
    maxFilesNum: 5,
    allowedFileTypes: ['image'],
    allowedFileExtensions: ['jpg', 'png', 'gif','ico'],
    showUpload: false,
    showRemove: false,
    showUploadProgress: false,
    browseIcon: "",
    browseLabel: "Upload",
    showCaption: false,
    browseOnZoneClick: true,
    overwriteInitial:false,
    minFileCount:1,
    maxFileCount:5,
    uploadAsync: false,
    uploadExtraData: uploadExtraOption,
    ajaxSettings: {headers: {"X-CSRFToken": csrftoken}}
}).on("filebatchselected", function(event,files){
    
    $("#file-input").fileinput("upload");
    
});

function uploadExtraOption(previewId, index)
{
    var ret={};
    op_type = $("#imageOperation").val();

    
    switch (op_type) {
        case "Compress":
	return {
	    img_op :  'compress',
	    compress_level:  $("#compressLevel").val(),
	    depth: $( "input[name=compress-depth]:checked" ).val()
	};
	break;
	
	case "Resize":
	return {
	    img_op :  'resize',
	    width: $("#inputX").val(),
	    height: $("#inputY").val(),
	    ignoreAspectRatio : $("#resizeIgnoreAspectRatio").prop("checked")
	};
	break;
	
	case "Convert":
	return {
	    img_op :  'convert',
	    img_type: $("select#convertType option:selected").val()
	};
	break;
	
	case "Transparent":
	return {
	    img_op :  'transparent'
	};
	break;
	
	case "Watermark":
	return {
	    img_op :  'watermark',
	    wotermarkText: $("#watermarkText").val(),
	    opacity:  $("#watermarkOpacity").val()
	};
	break;
	
	case "Animate":
	return {
	    img_op :  'animate',
	    interval :  $("#timeInterval").val()
	};
	break;
	default:
	ret = { img_op:'compress', compress_level:7, depth:8};
	}
    
    return ret;
}

$("#compress button").click(function(){

    // alert($.fn.fileinput);
    
    // $("form.imag-op") 
    // add compress image operation
    
});

