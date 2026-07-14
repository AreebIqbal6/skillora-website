"""Kill the Framer badge by patching index.html"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Override the CSS so the container is hidden
badge_kill_css = """
<style id="badge-kill">
  #__framer-badge-container,
  [id*="framer-badge"],
  [class*="framer-badge"],
  div[style*="z-index:2147480000"],
  div[style*="z-index: 2147480000"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
</style>
"""

# 2. Also override the inline CSS that Framer sets on the badge container
content = content.replace(
    '#__framer-badge-container{pointer-events:none;width:100%;z-index:calc(var(--infinity,2147480000));justify-content:flex-end;padding:20px;display:flex;position:fixed;bottom:0}',
    '#__framer-badge-container{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}'
)

# 3. Inject JS killer that runs immediately on DOM ready
badge_kill_js = """
<script>
// Kill Framer badge instantly
(function killBadge(){
  function remove(){
    var el = document.getElementById('__framer-badge-container');
    if(el){ el.remove(); return; }
    // Also try by z-index pattern
    var all = document.querySelectorAll('[style]');
    for(var i=0;i<all.length;i++){
      if(all[i].style.zIndex == '2147483647' || all[i].style.zIndex == '2147480000'){
        all[i].remove();
      }
    }
  }
  remove();
  document.addEventListener('DOMContentLoaded', remove);
  window.addEventListener('load', remove);
  // Keep watching for dynamic injection
  var obs = new MutationObserver(function(mutations){
    mutations.forEach(function(m){
      m.addedNodes.forEach(function(node){
        if(node.id === '__framer-badge-container' || 
           (node.style && (node.style.zIndex == '2147483647' || node.style.zIndex == '2147480000'))){
          node.remove();
        }
      });
    });
  });
  obs.observe(document.documentElement, {childList:true, subtree:true});
})();
</script>
"""

# Inject CSS at end of head
content = content.replace('</head>', badge_kill_css + badge_kill_js + '\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Badge killed.")
