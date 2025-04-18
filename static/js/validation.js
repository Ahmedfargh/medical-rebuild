function validate_email(email){
    const emailRegx=/^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegx.test(email);
}
function validate_phone(phone){
    const phoneRegx=/^\d{11}$/
    return phoneRegx.test(phone);
}
