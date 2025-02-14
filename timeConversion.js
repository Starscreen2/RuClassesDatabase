
// Function to convert military time to standard time
function convertMilitaryToStandard(militaryTime) {
    if (!militaryTime) return "N/A";
    
    const [hours, minutes] = militaryTime.split(':').map(Number);
    const period = hours >= 12 ? 'PM' : 'AM';
    const standardHours = hours % 12 || 12;
    
    return `${standardHours}:${minutes.toString().padStart(2, '0')} ${period}`;
}

// Function to convert standard time to military time
function convertStandardToMilitary(standardTime) {
    if (!standardTime) return "N/A";
    
    const [time, period] = standardTime.split(' ');
    let [hours, minutes] = time.split(':').map(Number);
    
    if (period === 'PM' && hours !== 12) hours += 12;
    if (period === 'AM' && hours === 12) hours = 0;
    
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

// Export functions
module.exports = {
    convertMilitaryToStandard,
    convertStandardToMilitary
};
