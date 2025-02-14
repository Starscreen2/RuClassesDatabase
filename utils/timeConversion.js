
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
