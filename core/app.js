
        const API_BASE = "http://127.0.0.1:8000";
        let capturedLogHistory = [];
        var activeThemeColor = "#00ff66"; // FIXED: BOUND GLOBALLY TO PREVENT TIMING ERRORS

        async function triggerGeneration() {

            const outBox = document.getElementById("generationOutput");
            outBox.innerHTML = "<span style='color: #666666;'>Streaming 512-HD tensor spaces...</span>";

            try {
                const response = await fetch(`${API_BASE}/v1/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        seed: document.getElementById("seedInput").value,
                        max_tokens: parseInt(document.getElementById("lengthInput").value),
                        temperature: parseFloat(document.getElementById("tempInput").value),
                        top_k: parseInt(document.getElementById("topkInput").value),
                        top_p: parseFloat(document.getElementById("toppInput").value)
                    })
                });
                const data = await response.json();


                if (response.ok) {
                    outBox.innerText = data.completed_text;
                    capturedLogHistory.push(data.completed_text);

                    // Update and render the visual stateful history buffer tracker
                    const logContainer = document.getElementById("historyLogView");
                    logContainer.innerHTML = ""; // Clear baseline empty string
                    capturedLogHistory.forEach((sceneText, idx) => {
                        // FIXED: PHASE M - STRUCTURAL VOXEL SCREENPLAY FORMATTING ENGINE
                        let slugHeader = "INT. THE ANTAGONIST VAULT - PALE MOONLIGHT";
                        if (sceneText.toLowerCase().includes("laboratory") || sceneText.toLowerCase().includes("machinery")) {
                            slugHeader = "EXT. LABORATORY ARCHIVE - NIGHT";
                        } else if (sceneText.toLowerCase().includes("frankenstein") || sceneText.toLowerCase().includes("monster")) {
                            slugHeader = "INT. FRANKENSTEIN CRUCIBLE - DAY";
                        }

                        logContainer.innerHTML += `
                        <div style="margin-bottom: 20px; border-bottom: 1px dashed #222222; padding-bottom: 12px; font-family: 'Courier New', monospace; font-size: 13px; text-align: left;">
                            <div style="color: #888888; font-weight: bold; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;">SCENE ${idx + 1} // ${slugHeader}</div>
                            <div style="color: #555555; font-style: italic; margin-bottom: 6px; padding-left: 10px;">The matrix pipeline variables update their weights onto disk tracks. Fontana commands the space.</div>
                            <div style="text-align: center; font-weight: bold; color: #ffffff; text-transform: uppercase; margin-top: 8px; margin-bottom: 2px;">FONTANA VOICE</div>
                            <div style="max-width: 70%; margin: 0 auto; text-align: left; color: #00ff66; border-left: 2px solid #222222; padding-left: 12px; font-weight: bold; transition: color 0.3s;" class="script-dialogue-text">${sceneText}</div>
                        </div>`;
                    });

                    const scriptTexts = document.querySelectorAll(".script-dialogue-text");
                    scriptTexts.forEach(el => { el.style.color = window.activeThemeColor || "#00ff66"; });
                    logContainer.scrollTop = logContainer.scrollHeight;


                    // SAFE TELEMETRY CONTAINER UPDATER LOOP
                    const telContainer = document.getElementById("matrixTelemetryView");
                    if (telContainer && data.telemetry) {
                        telContainer.style.color = window.activeThemeColor || "#00ff66";

                        telContainer.innerHTML = '\n=== MATRIX VECTOR STATUS ===\n' +
                            '[HIDDEN_UNITS] : ' + data.telemetry.hidden_dimensions + ' HD Layer\n' +
                            '[VOCAB_SIZE]   : ' + data.telemetry.vocabulary_size + ' Active Vectors\n' +
                            '[TOKEN_EVAL]   : Generated ' + data.telemetry.generated_token_count + ' subwords in RAM\n' +
                            '[TOKEN_IDS]    : [' + data.telemetry.prompt_token_ids.join(" -> ") + ']\n' +
                            '============================';

                        // FIXED: PHASE Q - REAL-TIME VISUAL PERFORMANCE DEBUGGER INDICATOR
                        const timeContainer = document.getElementById("latencyTracker");
                        if (timeContainer && data.telemetry.latency_ms !== undefined) {
                            timeContainer.innerText = 'LATENCY: ' + data.telemetry.latency_ms + 'ms';
                            timeContainer.style.color = window.activeThemeColor || "#00ff66";
                        }
                    }

                    // FIXED: PHASE L REAL-TIME TELEMETRY GRAPH VISUALIZER BARS ENGINE
                    const graphContainer = document.getElementById("telemetryGraphBars");
                    if (graphContainer && data.telemetry && data.telemetry.prompt_token_ids) {
                        graphContainer.innerHTML = ""; // Clear baseline empty strings
                        const tIds = data.telemetry.prompt_token_ids;
                        const currentColor = window.activeThemeColor || "#00ff66";

                        tIds.forEach(function(tokenId) {
                            // Map token ID integer values safely to an analytical visual bar height bounds percentage
                            const normalizedHeight = Math.min(100, Math.max(10, (tokenId / 107) * 100));
                            graphContainer.innerHTML += '<div style="width: 12px; height: ' + normalizedHeight + '%; background-color: ' + currentColor + '; min-width: 12px; transition: height 0.2s;" title="Token ID: ' + tokenId + '"></div>';
                        });
                    }

                    // FIXED: PHASE R REAL-TIME PARAMETER WEIGHT GRAPH NODE CANVAS ENGINE
                    const canvas = document.getElementById("weightNodeCanvas");
                    if (canvas && data.telemetry && data.telemetry.prompt_token_ids) {
                        const ctx = canvas.getContext("2d");
                        const tIds = data.telemetry.prompt_token_ids;
                        const currentColor = window.activeThemeColor || "#00ff66";

                        // Clear previous matrix projection frame safely
                        ctx.clearRect(0, 0, canvas.width, canvas.height);

                        if (tIds.length > 0) {
                            const padding = 30;
                            const usableWidth = canvas.width - (padding * 2);
                            const stepX = tIds.length > 1 ? usableWidth / (tIds.length - 1) : usableWidth;

                            let nodeCoordinates = [];

                            // Map token IDs into geometric coordinate points
                            tIds.forEach(function(tokenId, index) {
                                const posX = padding + (index * stepX);
                                // Alternating wave patterns to create an advanced neural constellation layout grid
                                const waveOffset = Math.sin(index * 1.5) * 25;
                                const posY = (canvas.height / 2) + waveOffset - ((tokenId / 194) * 35);
                                nodeCoordinates.push({ x: posX, y: posY, id: tokenId });
                            });

                            // Draw vector constellation trace lines
                            ctx.beginPath();
                            ctx.strokeStyle = currentColor;
                            ctx.lineWidth = 1;
                            ctx.setLineDash([2, 4]); // Brutalist dashed mapping tracks

                            nodeCoordinates.forEach(function(pt, idx) {
                                if (idx === 0) ctx.moveTo(pt.x, pt.y);
                                else ctx.lineTo(pt.x, pt.y);
                            });
                            ctx.stroke();
                            ctx.setLineDash([]); // Reset line style

                            // Draw the parameter weight node intersection points
                            nodeCoordinates.forEach(function(pt) {
                                ctx.beginPath();
                                ctx.arc(pt.x, pt.y, 4, 0, 2 * Math.PI);
                                ctx.fillStyle = "#000000";
                                ctx.fill();
                                ctx.strokeStyle = currentColor;
                                ctx.lineWidth = 2;
                                ctx.stroke();

                                // Print tiny brutalist token ID tags right above nodes
                                ctx.fillStyle = "#555555";
                                ctx.font = "9px monospace";
                                ctx.fillText(pt.id, pt.x - 6, pt.y - 8);
                            });
                        }
                    }

                    // FIXED: PHASE S STRUCTURAL SANDBOX VOXEL GRID CALCULATOR ENGINE
                    const voxelGrid = document.getElementById("sandboxVoxelGrid");
                    if (voxelGrid && data.completed_text) {
                        voxelGrid.innerHTML = ""; // Clear baseline frames
                        const txt = data.completed_text.toLowerCase();
                        const currentColor = window.activeThemeColor || "#00ff66";

                        // Parse screenplay patterns to derive a target structural coordinate matrix axis index
                        let activeCellIndex = 0;
                        if (txt.includes("alistair") || txt.includes("brain")) activeCellIndex = 3;
                        if (txt.includes("fontana") || txt.includes("system")) activeCellIndex = 5;
                        if (txt.includes("the") || txt.includes("and")) activeCellIndex = (data.tokens_evaluated % 16);

                        // Dynamically render a clean 4x4 matrix block layout space
                        for (let cellIdx = 0; cellIdx < 16; cellIdx++) {
                            const isNodeLit = (cellIdx === activeCellIndex);
                            const cellBg = isNodeLit ? currentColor : "#070707";
                            const cellTextColor = isNodeLit ? "#000000" : "#333333";
                            const cellBorder = isNodeLit ? '1px solid ' + currentColor : '1px solid #151515';

                            voxelGrid.innerHTML += `
                            <div style="background: ${cellBg}; border: ${cellBorder}; padding: 10px; font-size: 10px; font-family: 'Courier New', monospace; font-weight: bold; text-align: center; color: ${cellTextColor}; transition: all 0.3s;" class="voxel-cell-node" data-lit="${isNodeLit}">
                                [V_${cellIdx}]
                            </div>`;
                        }
                    }
                } else {





                    outBox.innerText = `❌ CORE ERROR: ${data.detail}`;
                }
            } catch (err) {
                outBox.innerText = `❌ BUS SECTOR BREAK: ${err.message}`;
            }
        }

        async function triggerTraining() {
            const outBox = document.getElementById("trainingOutput");
            outBox.innerHTML = "<span style='color: #666666;'>Compressing text stream into memory cells...</span>";

            try {
                const response = await fetch(`${API_BASE}/v1/train`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: document.getElementById("trainInput").value })
                });
                const data = await response.json();
                if (response.ok) {
                    outBox.innerHTML = `<span style='color: #00ff66;'>🌟 HARVEST COMPLETE: ${data.message}</span>\nWords processing: ${data.words_processed}`;
                    document.getElementById("trainInput").value = "";
                } else {
                    outBox.innerText = `❌ BOUNDARY ERROR: ${data.detail}`;
                }
            } catch (err) {
                outBox.innerText = `❌ BUS SECTOR BREAK: ${err.message}`;
            }
        }

        function exportToMarkdown() {
            if (capturedLogHistory.length === 0) {
                alert("Vault stream empty! Generate text blocks before exporting.");
                return;
            }

            // Format logs cleanly into structured screenplay blocks
            let markdownContent = `# FONTANA SCENARIO LOG\n\nGenerated via Antagonist.Core\n\n---\n\n`;
            capturedLogHistory.forEach((block, index) => {
                markdownContent += `### SEQUENCE ${index + 1}\n\n${block}\n\n`;
            });

            const blob = new Blob([markdownContent], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `fontana_vault_scene_${Date.now()}.md`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        function toggleVisualTheme() {
            const bodyNode = document.getElementById("vaultBody");
            if (bodyNode.classList.contains("theme-antagonist")) {
                bodyNode.classList.remove("theme-antagonist");
                bodyNode.classList.add("theme-opium");
                window.activeThemeColor = "#ff0055"; // Bound to window scope safely
            } else {
                bodyNode.classList.remove("theme-opium");
                bodyNode.classList.add("theme-antagonist");
                window.activeThemeColor = "#00ff66"; // Bound to window scope safely
            }
            const scriptTexts = document.querySelectorAll(".script-dialogue-text");
            scriptTexts.forEach(el => { el.style.color = window.activeThemeColor; });

            // Force intermediate canvas redraw to hot-swap constellation strings on click passes
            const canvas = document.getElementById("weightNodeCanvas");
            if (canvas && window.capturedLogHistory && window.capturedLogHistory.length > 0) {
                const ctx = canvas.getContext("2d");
                ctx.strokeStyle = window.activeThemeColor;
                // Simple stroke repaint to map color layout state changes
                ctx.stroke();
            }

            // Force dynamic voxel grid cell recoloring on active theme switches
            const litVoxels = document.querySelectorAll(".voxel-cell-node");
            litVoxels.forEach(function(el) {
                if (el.getAttribute("data-lit") === "true") {
                    el.style.backgroundColor = window.activeThemeColor;
                    el.style.borderColor = window.activeThemeColor;
                }
            });
        }

        // FIXED: PHASE U ASYNCHRONOUS THREAD-ISOLATED SCRATCHPAD CONTROLLER LOOP
        async function triggerScratchpadPass() {
            const outBox = document.getElementById("scratchpadOutput");
            outBox.innerHTML = "<span style='color: #666666;'>Processing air-gapped memory thread lane...</span>";

            try {
                const response = await fetch(`${API_BASE}/v1/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        seed: document.getElementById("scratchpadInput").value,
                        max_tokens: 30, // Localized short-burst parameter length
                        session_id: "isolated_scratch_lane", // FIXED: FORCE AIR-GAPPED STATE ROUTING CHANNEL
                        temperature: parseFloat(document.getElementById("tempInput").value),
                        top_k: parseInt(document.getElementById("topkInput").value),
                        top_p: parseFloat(document.getElementById("toppInput").value)
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    outBox.innerText = data.completed_text;
                } else {
                    outBox.innerText = `❌ CHANNEL ERROR: ${data.detail}`;
                }
            } catch (err) {
                outBox.innerText = `❌ BUS SECTOR BREAK: ${err.message}`;
            }
        }

