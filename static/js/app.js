// Funcionalidades generales de la aplicación EcoAnalyzer Web

// Configuración global
const CONFIG = {
    colors: {
        primary: '#601E88',
        secondary: '#2cb67d',
        accent: '#7f5af0',
        success: '#2cb67d',
        warning: '#f9ca24',
        danger: '#ff6b6b'
    }
};

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Auto-dismiss alerts después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Agregar loading states a los formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
            }
        });
    });

    // Validación de formularios en tiempo real
    const inputs = document.querySelectorAll('.custom-input');
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

// Validación de campos
function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    
    // Limpiar errores previos
    clearFieldError(event);
    
    // Validaciones específicas
    if (field.required && !value) {
        showFieldError(field, 'Este campo es obligatorio');
        return false;
    }
    
    if (field.type === 'number' && value) {
        const num = parseFloat(value);
        if (isNaN(num) || num < 0) {
            showFieldError(field, 'Debe ser un número positivo');
            return false;
        }
    }
    
    if (field.name === 'precio' && value) {
        const precio = parseFloat(value);
        if (precio <= 0) {
            showFieldError(field, 'El precio debe ser mayor a 0');
            return false;
        }
    }
    
    if (field.name === 'vendido' && value) {
        const vendido = parseInt(value);
        if (vendido <= 0) {
            showFieldError(field, 'La cantidad debe ser mayor a 0');
            return false;
        }
    }
    
    return true;
}

function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    // Remover mensaje de error previo
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
    
    // Agregar nuevo mensaje de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(event) {
    const field = event.target;
    field.classList.remove('is-invalid');
    
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Utilidades para notificaciones
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss después de 5 segundos
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Formateo de números
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 2
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('es-CO').format(number);
}

// Validación de fecha
function validateDate(dateString) {
    const date = new Date(dateString);
    const today = new Date();
    
    if (isNaN(date.getTime())) {
        return { valid: false, message: 'Fecha inválida' };
    }
    
    if (date > today) {
        return { valid: false, message: 'La fecha no puede ser futura' };
    }
    
    return { valid: true };
}

// Funciones de utilidad para localStorage
function saveToStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (error) {
        console.error('Error guardando en localStorage:', error);
        return false;
    }
}

function loadFromStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Error cargando desde localStorage:', error);
        return null;
    }
}

// Funciones para manejo de formularios
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        
        // Limpiar errores de validación
        const invalidFields = form.querySelectorAll('.is-invalid');
        invalidFields.forEach(field => {
            field.classList.remove('is-invalid');
        });
        
        const errorMessages = form.querySelectorAll('.invalid-feedback');
        errorMessages.forEach(error => error.remove());
    }
}

// Funciones para animaciones
function fadeIn(element, duration = 300) {
    element.style.opacity = '0';
    element.style.display = 'block';
    
    let start = Date.now();
    
    function animate() {
        let timePassed = Date.now() - start;
        let progress = timePassed / duration;
        
        if (progress > 1) progress = 1;
        
        element.style.opacity = progress;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

function fadeOut(element, duration = 300) {
    let start = Date.now();
    
    function animate() {
        let timePassed = Date.now() - start;
        let progress = timePassed / duration;
        
        if (progress > 1) progress = 1;
        
        element.style.opacity = 1 - progress;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            element.style.display = 'none';
        }
    }
    
    requestAnimationFrame(animate);
}

// Confirmación de acciones destructivas
function confirmAction(message = '¿Estás seguro?') {
    return confirm(message);
}

// Debug helper (solo en desarrollo)
function debug(message, data = null) {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log(`[EcoAnalyzer] ${message}`, data);
    }
}

// Exportar funciones globalmente
window.EcoAnalyzer = {
    showNotification,
    formatCurrency,
    formatNumber,
    validateDate,
    saveToStorage,
    loadFromStorage,
    resetForm,
    fadeIn,
    fadeOut,
    confirmAction,
    debug
};