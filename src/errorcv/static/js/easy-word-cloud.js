


var fill = d3.scale.category20();

// windowオブジェクトのプロパティにすることでmakeWordCloudを他のファイルから呼び出せるようにする
window.makeWordCloud = function(data, parent_elem, svgscale, svg_class, font, rotate_word, my_colors){

      function draw(words) {
        d3.select(parent_elem).append("svg")
            .attr("width", svgscale)
            .attr("height", svgscale)
            .attr("class", svg_class)
            .attr("preserveAspectRatio", "xMinYMin meet")
            .attr("viewBox", "0 0 500 500")
            .classed("svg-content-responsive", true)
          .append("g")
            .attr("transform", "translate(" + svgscale / 2 + "," + svgscale / 2 + ")")
          .selectAll("text")
            .data(words)
          .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("font-family", font)
            .style("fill", function(d, i) { if(my_colors){ return my_colors(i); }else{ return fill(i); } })
            .attr("text-anchor", "middle")
            .attr("class", "test")
            .attr("transform", function(d) {
              return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
      }

      if(svg_class){ d3.select("." + svg_class).remove() }
      else{ d3.select("svg").remove() }

      var data_max =  d3.max(data, function(d){ return d.value } );
      var sizeScale = d3.scale.linear().domain([0, data_max]).range([0, 1])

      data = data.map(function(d) {
        return {text: d.word, size: 10 + sizeScale(d.value) * 90};
      })

      var layout = d3.layout.cloud().size([svgscale, svgscale])
        .words(data)
        .padding(5)
        .fontSize(function(d) { return d.size; })
        
      // 単語を回転させるか否か
      if(!rotate_word){ layout.rotate(function() { return ~~(Math.random() * 2) * 90; }) }
        
      layout
        .on("end", draw)
        .start();

        d3.selectAll("text").on("click", function() {
          //check if node is already selected
          var text = d3.select(this)//.select("text");
          console.log(text, text[0][0].innerHTML)
          if (text.classed("selectedText")) {
            text.classed("selectedText", false);
            //Remove class selectedNode
          } else {
            text.classed("selectedText", true);    
            //Adds class selectedNode
          }
          getRedditData(text[0][0].innerHTML);
        });

        cloudLoading(false)
  }
