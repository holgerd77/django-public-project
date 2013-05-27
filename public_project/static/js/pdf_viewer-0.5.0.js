var PDFViewer = new function() {
   
   // Set to STANDARD or LEGACY
   this.viewer = null;
   
   this.pageNum = 1;
   this.numPages = null;
   this.searchString = '';
   this.url = '';
   
   // Current
   this.pdfDoc = null,
   this.scale = null,
   this.canvas = null,
   this.ctx = null;  
   
   
   this.initStandard = function() {
      this.pdfDoc = null,
      this.scale = 1.0,
      this.canvas = document.getElementById('the-canvas'),
      this.ctx = this.canvas.getContext('2d');
      PDFJS.disableWorker = true; 
   }
   
   this.initLegacy = function() {
      
   }
   
   this.getUrlVars = function() {
      var vars = {};
      var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
         vars[key] = value;
      });
      return vars;
   }   
   
   this.styleComments = function() {
      $('.page_comment .comment_relations').css('display', 'none');
      $('.page_comment .comment_text').css('display', 'none');
      $('.page_comment .comment_header').css('background-color', '#f9f9f9');
      $('.page_comment .comment_page').css('background-color', '#ddd');
      $('.page_comment .comment_page').css('color', '#555');
      
      $('.comment_page_' + this.pageNum + ' .comment_relations').css('display', 'block');
      $('.comment_page_' + this.pageNum + ' .comment_text').css('display', 'block');
      $('.comment_page_' + this.pageNum + ' .comment_header').css('background-color', '#fdd');
      $('.comment_page_' + this.pageNum + ' .comment_page').css('background-color', '#c77');
      $('.comment_page_' + this.pageNum + ' .comment_page').css('color', '#fff');
      
      $('.page_comment').css('display', 'block');
   }
   
   
   this.renderPageStandard = function(num) {
      $('#pdf_load_warning').css('display', 'none');
      // Using promise to fetch the page
      this.pdfDoc.getPage(num).then(function(page) {
         var viewport = page.getViewport(1.0);
         scale = $('#pdf-outer-div').width() / viewport.width;
         viewport = page.getViewport(scale);
         PDFViewer.canvas.height = viewport.height;
         PDFViewer.canvas.width = viewport.width;
    
         // Render PDF page into canvas context
         var renderContext = {
            canvasContext: PDFViewer.ctx,
            viewport: viewport,
            textLayer: CustomTextLayer
         };
        
         textDivs = [];
          
         page.render(renderContext).then(
            function(data) {
               page.getTextContent().then(
                  function textContentResolved(data) {
                     if (PDFViewer.searchString != '') {
                        $('#text-layer').empty();
                        CustomTextLayer.insertDivContent(data);
                        CustomTextLayer.renderLayer();
                        $('#text-layer > div').highlight(PDFViewer.searchString.replace(/&quot;/g, ''));
                     }
                  }
              );
            }
         )
      });
      
      // Update page counters
      this.pageNum = num;
      $('#page_num').val(this.pageNum);
      document.getElementById('page_count').textContent = this.numPages;
      
      this.styleComments();
   }   
   
   
   this.renderPageLegacy = function(num) {
      $('#pdf_load_warning').css('display', 'none');
      $('#documentCarousel').carousel(num-1);
      this.pageNum = num;
      $('#page_num').val(this.pageNum);
      document.getElementById('page_count').textContent = this.numPages;
      
      this.styleComments();
   }
   
   
   this.renderPage = null;
   
   
   this.loadPage = function(viewer, url, searchString, searchPageNum) {
      this.viewer = viewer,
      this.url = url;
      this.searchString = searchString;
      
      var page = this.getUrlVars()["page"];
      if (page){
         this.pageNum = page; 
      } else {
         if(searchPageNum) {
            this.pageNum = searchPageNum;
         }
      }
      
      $('#documentCarousel').carousel({ interval: false });
      
      if (this.viewer == 'STANDARD') {
         this.renderPage = this.renderPageStandard;
         PDFViewer.initStandard();
         PDFJS.getDocument(this.url).then(function getPdfHelloWorld(_pdfDoc) {
            PDFViewer.pdfDoc = _pdfDoc;
            PDFViewer.numPages = PDFViewer.pdfDoc.numPages;
            PDFViewer.renderPage(PDFViewer.pageNum);
         });
      } else {
         this.renderPage = this.renderPageLegacy;
         this.numPages = $('.carousel-inner img').length;
         this.renderPage(this.pageNum);
      }
      
      $('#pdf_navi_left').click(function() {
         if (PDFViewer.pageNum <= 1)
            var num = PDFViewer.numPages;
         else
            var num = PDFViewer.pageNum - 1;
         PDFViewer.renderPage(num);
         return false;
      });
  
      $('#pdf_navi_right').click(function() {
         if (PDFViewer.pageNum >= PDFViewer.numPages)
            var num = 1;
         else
            var num = PDFViewer.pageNum + 1;
         PDFViewer.renderPage(num);
         return false;
      });
      
      $('#page_num').keypress(function(e) {
         code= (e.keyCode ? e.keyCode : e.which);
         if (code == 13) {
            var num = parseInt($(this).val());
            PDFViewer.renderPage(num);
            $(this).val(val);
            $(this).blur();
            e.preventDefault();
         }
      });
   } 
}




$(document).ready(function() {
  
  var rtime = new Date(1, 1, 2000, 12,00,00);
  var timeout = false;
  var delta = 200;
  $(window).resize(function() {
      rtime = new Date();
      if (timeout === false) {
          timeout = true;
          setTimeout(resizeend, delta);
      }
  });
  
  function resizeend() {
      if (new Date() - rtime < delta) {
          setTimeout(resizeend, delta);
      } else {
          timeout = false;
          PDFViewer.renderPage(PDFViewer.pageNum);
      }               
  }
});
