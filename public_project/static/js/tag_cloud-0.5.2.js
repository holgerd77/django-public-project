var tc_div_id = null;
var tc_document_id = null;
var tc_base_url = null;
var tc_height = null;


function load_tag_cloud(div_id, document_id, content_type, base_url, height) {
   tc_div_id = div_id;
   tc_document_id = document_id;
   tc_content_type = content_type;
   tc_base_url = base_url;
   tc_height = height;
   
   $(div_id).empty();
   
   var width = $(div_id).width();
   var half_width = Math.round(width/2);
   var half_height = Math.round(height/2) + 5;
   
   function draw_tag_cloud(words) {
      d3.select(div_id).append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + half_width + "," + half_height + ")")
      .selectAll("text")
      .data(words)
      .enter().append("text")
      .style("font-size", function(d) { return d.size + "px"; })
      .style("font-family", "Arial")
      .style("fill", function(d, i) { return d.color; })
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
         return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.text; })
      .on("click", function(d) {
         window.location = base_url + "?q=" + encodeURIComponent(d.text);
      });
   }
  
   $.ajax({
      type: 'POST',
      url: '/xhr/document_tags/',
      dataType: 'json',
      data: {
         csrfmiddlewaretoken: csrf_token,
         document_id: document_id,
         content_type: content_type,
      },
      success: function(data) {
         if (data.length < 1) {
            $(div_id).append('<div style="padding:20px;color:#aaa;">' + tag_cloud_not_available_msg + '</div>');
         } else {
            d3.layout.cloud()
            .size([width, height])
            .words(data.map(function(d) {
               return { text: d.text, size:d.size, color: d.color }
            }))
            .rotate(0)
            .font("Arial")
            .fontSize(function(d) { return d.size; })
            .startPoint([150, 70])
            .on("end", draw_tag_cloud)
            .start();
         }
      },
      error: function() {
         $(div_id).append('<div style="padding:20px;color:#aaa;">' + tag_cloud_error_msg + '</div>');
      }
   })
}


var tc_rtime = new Date(1, 1, 2000, 12,00,00);
var tc_timeout = false;
var tc_delta = 200;
$(window).resize(function() {
   tc_rtime = new Date();
   if (tc_timeout === false) {
      tc_timeout = true;
      setTimeout(tc_resizeend, tc_delta);
   }
});
  
function tc_resizeend() {
   if (new Date() - tc_rtime < tc_delta) {
      setTimeout(tc_resizeend, tc_delta);
   } else {
      tc_timeout = false;
      if(tc_div_id) {
         load_tag_cloud(tc_div_id, tc_document_id, tc_content_type, tc_base_url, tc_height);
      }
   }            
}
