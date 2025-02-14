
// Converts a 24-hour time string (e.g., "14:30") to standard AM/PM time (e.g., "2:30 PM")
function convertTime(timeStr) {
    // Split hours and minutes
    const [hourStr, minute] = timeStr.split(':');
    let hour = parseInt(hourStr, 10);
    
    // Determine AM/PM
    const suffix = hour >= 12 ? 'PM' : 'AM';
    
    // Convert hour from 24-hour to 12-hour format, handling midnight and noon
    hour = hour % 12 || 12;
    
    return `${hour}:${minute} ${suffix}`;
}

// Example usage:
console.log(convertTime("00:00")); // Expected output: "12:00 AM"
console.log(convertTime("12:00")); // Expected output: "12:00 PM"
console.log(convertTime("14:30")); // Expected output: "2:30 PM"

// ...existing code or exports...
module.exports = { convertTime };
