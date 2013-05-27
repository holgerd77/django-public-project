/*
 * This script is based on the web viewer of the pdf.js project and uses various parts
 * of its code base
 * https://github.com/mozilla/pdf.js/blob/master/web/viewer.js 
 */

/* -*- Mode: Java; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*- */
/* vim: set shiftwidth=2 tabstop=2 autoindent cindent expandtab: */
/* Copyright 2012 Mozilla Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


var textDivs = [];

var CustomTextLayer = {
  
  beginLayout: function() {
  },

  endLayout: function() {
  },
  
  appendText: function(geom) {
    var textDiv = document.createElement('div');

    // vScale and hScale already contain the scaling to pixel units
    var fontHeight = geom.fontSize * geom.vScale;
    textDiv.dataset.canvasWidth = geom.canvasWidth * geom.hScale;
    textDiv.dataset.fontName = geom.fontName;

    textDiv.style.fontSize = fontHeight + 'px';
    textDiv.style.fontFamily = geom.fontFamily;
    textDiv.style.left = geom.x + 'px';
    textDiv.style.top = (geom.y - fontHeight + 2) + 'px';

    // The content of the div is set in the `setTextContent` function.

    textDivs.push(textDiv);
  },
  
  insertDivContent: function(data) {
    var bidiTexts = data.bidiTexts;

    for (var i = 0; i < bidiTexts.length; i++) {
      var bidiText = bidiTexts[i];
      var textDiv = textDivs[i];
      textDiv.textContent = bidiText.str;
    }
  },
  
  renderLayer: function() {
    var textLayerDiv = document.getElementById('text-layer');
    var canvas = document.getElementById('the-canvas');
    var ctx = canvas.getContext('2d');

    // No point in rendering so many divs as it'd make the browser unusable
    // even after the divs are rendered
    var MAX_TEXT_DIVS_TO_RENDER = 100000;
    if (textDivs.length > MAX_TEXT_DIVS_TO_RENDER)
      return;

    for (var i = 0, ii = textDivs.length; i < ii; i++) {
      var textDiv = textDivs[i];

      ctx.font = textDiv.style.fontSize + ' ' + textDiv.style.fontFamily;
      var width = ctx.measureText(textDiv.textContent).width;

      if (width > 0) {
        var textScale = textDiv.dataset.canvasWidth / width;

        //CustomStyle.setProp('transform' , textDiv,
        //  'scale(' + textScale + ', 1)');
        //CustomStyle.setProp('transformOrigin' , textDiv, '0% 0%');

        textLayerDiv.appendChild(textDiv);
      }
    }
}
  
};