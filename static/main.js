document.addEventListener("DOMContentLoaded", function () {
    // Sidebar toggle
    const menuToggle = document.getElementById("menuToggle");
    const sidebar = document.getElementById("sidebar");
    const sidebarOverlay = document.getElementById("sidebarOverlay");
    const sidebarClose = document.getElementById("sidebarClose");

    menuToggle.addEventListener("click", () => {
        sidebar.classList.add("open");
        sidebarOverlay.style.display = "block";
    });

    sidebarClose.addEventListener("click", () => {
        sidebar.classList.remove("open");
        sidebarOverlay.style.display = "none";
    });

    sidebarOverlay.addEventListener("click", () => {
        sidebar.classList.remove("open");
        sidebarOverlay.style.display = "none";
    });

    // Handle dynamic block addition to workspace
    const addButtons = document.querySelectorAll(".block-btn");
    const workspaceContainer = document.getElementById("workflowContainer");
    const emptyState = document.getElementById("workspaceEmpty");

    addButtons.forEach(btn => {
        // Skip if button is a link (like Mail Agent)
        if (btn.tagName.toLowerCase() === 'a') return;

        btn.addEventListener("click", (e) => {
            const block = e.target.closest(".ai-block");
            const clone = block.cloneNode(true);
            clone.classList.add("cloned-block");

            // Remove the plus button to prevent infinite nesting
            const cloneBtn = clone.querySelector(".block-actions");
            if (cloneBtn) cloneBtn.remove();

            workspaceContainer.appendChild(clone);
            emptyState.style.display = "none";
        });
    });
});
