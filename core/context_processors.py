def business_info(request):
    """Inject NWZ's business details into every template's context."""
    return {
        'BUSINESS': {
            'name': 'NWZ',
            'full_name': 'NWZ Nutrition & Wellness',
            'tagline': 'Personalised nutrition, backed by science.',
            'owner_name': 'Chizitere Chibuzo-Eke',
            'owner_credentials': 'BSc. Human Nutrition & Dietetics, M.IDN',
            'owner_role': 'Registered Dietitian Nutritionist',
            'years_experience': 2,
            'address': '22 Marcel Anaenugu Crescent, Farm Rd, Rumuosi, Rivers State',
            'phone': '08081187444',
            'phone_display': '0808 118 7444',
            'whatsapp': '08081187444',
            'whatsapp_link': 'https://wa.me/2348081187444',
            'email': 'chiziterechibuzo@gmail.com',
            'hours': 'Open every day · 9:00 AM – 5:00 PM',
            'hours_note': 'Closed on public holidays. Book ahead to guarantee your slot.',
            'session_modes': 'In-person and online sessions available',
        }
    }
