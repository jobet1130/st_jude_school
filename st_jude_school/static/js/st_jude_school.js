class AppCore {
    constructor() {
        this.debugMode = true; // Set to false for production
        this.init();
    }

    init() {
        this.log("AppCore initialized.");
        this.bindGlobalEvents();
        this.autoInstantiateClasses();
    }

    log(message, level = 'info') {
        if (this.debugMode) {
            const timestamp = new Date().toISOString();
            switch (level) {
                case 'info':
                    console.info(`[AppCore][INFO][${timestamp}] ${message}`);
                    break;
                case 'warn':
                    console.warn(`[AppCore][WARN][${timestamp}] ${message}`);
                    break;
                case 'error':
                    console.error(`[AppCore][ERROR][${timestamp}] ${message}`);
                    break;
                default:
                    console.log(`[AppCore][DEBUG][${timestamp}] ${message}`);
            }
        }
    }

    bindGlobalEvents() {
        // Example: document.addEventListener('DOMContentLoaded', () => this.log('DOM Ready'));
        this.log("Global events bound.");
    }

    autoInstantiateClasses() {
        // Placeholder for auto-instantiation logic
        this.log("Auto-instantiating classes (if any).");
    }
}

class AjaxService {
    constructor() {
        if (typeof jQuery === 'undefined') {
            console.error("AjaxService requires jQuery to be loaded.");
            throw new Error("jQuery not found.");
        }
        this.isLoading = false;
    }

    _ajax(method, url, data, onSuccess, onError, beforeSendCallback, completeCallback) {
        this.isLoading = true;
        if (beforeSendCallback) beforeSendCallback();

        $.ajax({
            url: url,
            method: method,
            data: data,
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            traditional: true, // For sending array data correctly
            beforeSend: function(xhr, settings) {
                // Add CSRF token for Django if available
                function getCookie(name) {
                    let cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        const cookies = document.cookie.split(';');
                        for (let i = 0; i < cookies.length; i++) {
                            const cookie = cookies[i].trim();
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: (response) => {
                this.isLoading = false;
                if (completeCallback) completeCallback();
                if (onSuccess) onSuccess(response);
            },
            error: (xhr, status, error) => {
                this.isLoading = false;
                if (completeCallback) completeCallback();
                console.error(`AJAX Error: ${method} ${url}`);
                console.error("Status:", status);
                console.error("Error:", error);
                console.error("Response Text:", xhr.responseText);
                try {
                    const errorResponse = JSON.parse(xhr.responseText);
                    if (onError) onError(errorResponse, xhr.status);
                } catch (e) {
                    if (onError) onError({ message: "An unexpected error occurred.", detail: xhr.responseText }, xhr.status);
                }
            }
        });
    }

    getRequest(url, onSuccess, onError, beforeSendCallback = null, completeCallback = null) {
        this._ajax('GET', url, {}, onSuccess, onError, beforeSendCallback, completeCallback);
    }

    postRequest(url, data, onSuccess, onError, beforeSendCallback = null, completeCallback = null) {
        this._ajax('POST', url, JSON.stringify(data), onSuccess, onError, beforeSendCallback, completeCallback);
    }

    // Example loading state methods
    onLoadingStart(callback) {
        // You can attach a UI update callback here
        // e.g., show a spinner
        this.loadingStartCallback = callback;
    }

    onLoadingComplete(callback) {
        // You can attach a UI update callback here
        // e.g., hide a spinner
        this.loadingCompleteCallback = callback;
    }
}
