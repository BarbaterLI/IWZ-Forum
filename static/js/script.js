// 主题切换功能
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    
    if (themeToggle) {
        const themeIcon = themeToggle.querySelector('i');
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
        const currentTheme = localStorage.getItem('theme');
        
        if (currentTheme === 'dark' || (!currentTheme && prefersDarkScheme.matches)) {
            document.body.classList.add('dark-mode');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
        
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            
            if (document.body.classList.contains('dark-mode')) {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
                localStorage.setItem('theme', 'dark');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
                localStorage.setItem('theme', 'light');
            }
        });
    }
    
    // 代码块复制功能
    function addCopyButtons() {
        const codeBlocks = document.querySelectorAll('pre code');
        codeBlocks.forEach(function(codeBlock) {
            // 创建包装容器
            const pre = codeBlock.parentElement;
            const wrapper = document.createElement('div');
            wrapper.className = 'code-block-wrapper';
            pre.parentNode.insertBefore(wrapper, pre);
            wrapper.appendChild(pre);
            
            // 创建复制按钮
            const button = document.createElement('button');
            button.className = 'copy-btn';
            button.textContent = '复制';
            button.setAttribute('aria-label', '复制代码');
            wrapper.appendChild(button);
            
            // 添加复制功能
            button.addEventListener('click', function() {
                const code = codeBlock.textContent;
                navigator.clipboard.writeText(code).then(function() {
                    // 复制成功
                    button.textContent = '已复制';
                    button.classList.add('copied');
                    
                    // 3秒后恢复原状
                    setTimeout(function() {
                        button.textContent = '复制';
                        button.classList.remove('copied');
                    }, 3000);
                }).catch(function(err) {
                    console.error('复制失败: ', err);
                    button.textContent = '复制失败';
                    setTimeout(function() {
                        button.textContent = '复制';
                    }, 3000);
                });
            });
        });
    }
    
    // 页面加载完成后添加复制按钮
    addCopyButtons();
});
