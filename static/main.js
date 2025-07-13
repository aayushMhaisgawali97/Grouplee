
    document.addEventListener("DOMContentLoaded", function () {
        const sidebar = document.getElementById("sidebar");
        const menuToggle = document.getElementById("menuToggle");
        const sidebarClose = document.getElementById("sidebarClose");
        const sidebarOverlay = document.getElementById("sidebarOverlay");

        function isMobileView() {
            return window.innerWidth <= 768;
        }

        function toggleSidebarListeners(enable) {
            if (enable) {
                menuToggle.addEventListener("click", openSidebar);
                sidebarClose.addEventListener("click", closeSidebar);
                sidebarOverlay.addEventListener("click", closeSidebar);
            } else {
                menuToggle.removeEventListener("click", openSidebar);
                sidebarClose.removeEventListener("click", closeSidebar);
                sidebarOverlay.removeEventListener("click", closeSidebar);
            }
        }

        function openSidebar() {
            sidebar.classList.add("active");
            sidebarOverlay.classList.add("active");
        }

        function closeSidebar() {
            sidebar.classList.remove("active");
            sidebarOverlay.classList.remove("active");
        }

        function checkView() {
            if (isMobileView()) {
                closeSidebar();
                toggleSidebarListeners(true);
            } else {
                sidebar.classList.remove("active");
                sidebarOverlay.classList.remove("active");
                toggleSidebarListeners(false);
            }
        }

        window.addEventListener("resize", checkView);
        checkView(); // initial check
    });
    // 🚀 Workspace block addition logic
function createWorkspaceBlock(data) {
    const block = document.createElement("div");
    block.className = "ai-block";
    block.innerHTML = `
        <div class="block-icon"><i class="fas fa-cube"></i></div>
        <div class="block-content">
            <h3 class="block-title">${data.title}</h3>
            <p class="block-description">${data.description}</p>
        </div>
    `;
    return block;
}

function updateWorkspaceDisplay() {
    const savedBlocks = JSON.parse(localStorage.getItem("workspaceBlocks") || "[]");
    workspaceContainer.innerHTML = "";
    if (savedBlocks.length === 0) {
        workspaceEmpty.style.display = "flex";
    } else {
        workspaceEmpty.style.display = "none";
        savedBlocks.forEach(data => {
            const block = createWorkspaceBlock(data);
            workspaceContainer.appendChild(block);
        });
    }
}

document.querySelectorAll(".block-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const aiBlock = btn.closest(".ai-block");
        const data = {
            title: aiBlock.getAttribute("data-title"),
            description: aiBlock.getAttribute("data-description"),
            type: aiBlock.getAttribute("data-type")
        };

        const existing = JSON.parse(localStorage.getItem("workspaceBlocks") || "[]");
        existing.push(data);
        localStorage.setItem("workspaceBlocks", JSON.stringify(existing));
        updateWorkspaceDisplay();
    });
});

updateWorkspaceDisplay();

