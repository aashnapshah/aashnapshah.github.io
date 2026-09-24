/* Masonry for the photo gallery.

   Places each figure into whichever column is currently shortest, using the
   width/height attributes so it never has to wait for an image to load.

   Why not CSS: multi-column with break-inside:avoid pushes a tall photo that
   cannot fit the remaining space into the next column and leaves the gap
   behind. It also fills column 1 top to bottom before starting column 2, which
   buries the first photos down the left edge. Shortest-column placement fixes
   both -- the opening figures land across the top row, in order.

   Without JS the CSS multi-column rules still apply, so the page degrades to
   the old layout rather than to nothing. */
(function () {
  var GAP = 9.6; // 0.6rem

  function layout(grid) {
    var figures = grid._figures || Array.prototype.slice.call(grid.querySelectorAll("figure"));
    grid._figures = figures;

    var width = grid.clientWidth;
    if (!width) return;
    var min = parseInt(grid.dataset.min, 10) || 150;
    var count = Math.max(1, Math.floor((width + GAP) / (min + GAP)));
    if (grid._count === count) return;
    grid._count = count;

    var cols = [], heights = [], i;
    for (i = 0; i < count; i++) {
      var col = document.createElement("div");
      col.className = "gallery__col";
      cols.push(col);
      heights.push(0);
    }

    var colWidth = (width - GAP * (count - 1)) / count;
    figures.forEach(function (fig) {
      var img = fig.querySelector("img");
      var w = parseFloat(img.getAttribute("width")) || 1;
      var h = parseFloat(img.getAttribute("height")) || 1;
      var shortest = heights.indexOf(Math.min.apply(null, heights));
      cols[shortest].appendChild(fig);
      heights[shortest] += (colWidth * h) / w + GAP;
    });

    grid.innerHTML = "";
    cols.forEach(function (col) { grid.appendChild(col); });
    grid.classList.add("is-laid-out");
  }

  /* Justified rows, for the small showcase block at the top.
     Shortest-column masonry cannot balance a dozen items across two columns --
     it leaves a few hundred pixels of white at the foot of the short one. Here
     each row is scaled to exactly fill the width, so every row is flush and the
     reading order is plainly left to right. */
  function layoutJustified(grid) {
    var figures = grid._figures || Array.prototype.slice.call(grid.querySelectorAll("figure"));
    grid._figures = figures;

    var width = grid.clientWidth;
    if (!width) return;
    if (grid._width === width) return;
    grid._width = width;

    var target = parseInt(grid.dataset.rowHeight, 10) || 260;
    var maxBig = parseInt(grid.dataset.bigHeight, 10) || 560;
    var rows = [], row = [], sum = 0, i;

    function closeRow(last) {
      if (row.length) rows.push({ items: row, sum: sum, last: last });
      row = [];
      sum = 0;
    }

    for (i = 0; i < figures.length; i++) {
      var img = figures[i].querySelector("img");
      var ratio = (parseFloat(img.getAttribute("width")) || 1) / (parseFloat(img.getAttribute("height")) || 1);
      // A photo marked big takes a row to itself. Rows are justified to one
      // shared height, so the only way to make a single photo larger than its
      // neighbours is to stop giving it any.
      if (figures[i].classList.contains("is-big")) {
        closeRow(false);
        rows.push({ items: [{ fig: figures[i], ratio: ratio }], sum: ratio, big: true });
        continue;
      }
      row.push({ fig: figures[i], ratio: ratio });
      sum += ratio;
      if (sum * target + GAP * (row.length - 1) >= width) closeRow(false);
    }
    closeRow(true);

    // The greedy pass often strands one or two photos on the final row, which
    // reads as a hole in an otherwise flush block. Merge that row back into
    // the one above and split the combined photos into two rows of roughly
    // equal aspect, so both justify to the full width.
    function makeRow(items, last) {
      var sum = items.reduce(function (t, it) { return t + it.ratio; }, 0);
      return { items: items, sum: sum, last: last };
    }
    if (rows.length > 1) {
      var tail = rows[rows.length - 1], above = rows[rows.length - 2];
      var tailWidth = tail.sum * target + GAP * (tail.items.length - 1);
      if (!tail.big && !above.big && tailWidth < width * 0.8) {
        var merged = above.items.concat(tail.items);
        var total = merged.reduce(function (t, it) { return t + it.ratio; }, 0);
        // Try every split and keep the most even one. Taking the first cut
        // past halfway would leave four similar photos as 3 + 1, which is the
        // stranded row all over again.
        var cut = 1, best = Infinity, running = 0, k;
        for (k = 1; k < merged.length; k++) {
          running += merged[k - 1].ratio;
          var gapness = Math.abs(running - (total - running));
          if (gapness < best) { best = gapness; cut = k; }
        }
        rows.splice(rows.length - 2, 2,
          makeRow(merged.slice(0, cut), false),
          makeRow(merged.slice(cut), true));
      }
    }

    grid.innerHTML = "";
    rows.forEach(function (r) {
      var available = width - GAP * (r.items.length - 1);
      var height = available / r.sum;
      // don't blow the final row up to full width if it holds only a couple
      if (r.last && height > target * 1.35) height = target;
      if (r.big) height = Math.min(height, maxBig);
      var el = document.createElement("div");
      el.className = "gallery__row" + (r.big ? " gallery__row--big" : "");
      r.items.forEach(function (item) {
        item.fig.style.width = (item.ratio * height).toFixed(2) + "px";
        el.appendChild(item.fig);
      });
      grid.appendChild(el);
    });
    grid.classList.add("is-laid-out");
  }

  function layoutAll() {
    Array.prototype.forEach.call(document.querySelectorAll(".gallery"), function (grid) {
      (grid.dataset.layout === "justified" ? layoutJustified : layout)(grid);
    });
  }

  layoutAll();

  var pending;
  window.addEventListener("resize", function () {
    clearTimeout(pending);
    pending = setTimeout(layoutAll, 120);
  });
})();
