document.getElementById('automationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const resumeFile = formData.get('resume');  // Assuming 'resume' is the file input field name

    // Step 1: Upload the resume file if it exists
    let resumePath = "";
    if (resumeFile && resumeFile.size > 0) {
        const uploadFormData = new FormData();
        uploadFormData.append('resume', resumeFile);

        try {
            const uploadResponse = await fetch('/api/upload', {
                method: 'POST',
                body: uploadFormData
            });
            const uploadResult = await uploadResponse.json();

            if (!uploadResponse.ok) {
                alert(uploadResult.error || "Failed to upload resume. Please check the file and try again.");
                return;
            }

            resumePath = uploadResult.path;  // Get the path to the uploaded resume file
        } catch (error) {
            console.error("File upload error:", error);
            alert("An error occurred while uploading the resume.");
            return;
        }
    }

    // Step 2: Start the automation
    const data = {
        username: formData.get('username'),
        password: formData.get('password'),
        keyword: formData.get('keyword'),
        max_applications: formData.get('max_applications'),
        filters: {
            today_only: formData.get('today_only') === 'on',
            third_party: formData.get('third_party') === 'on'
        },
        resume_path: resumePath  // Pass the resume file path if uploaded
    };

    try {
        const response = await fetch('/api/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message || "Automation started successfully!");
            window.location.href = "/status";  // Redirect to status page upon success
        } else {
            const errorResult = await response.json();
            alert(errorResult.error || "Failed to start automation. Please check your input.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while starting automation.");
    }
});
