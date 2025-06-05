module.exports = {
    content: [
        './templates/**/*.html',
        './**/templates/**/*.html',
        './**/forms.py',
        './**/views.py',
    ],
    theme: {
        extend: {
            colors: {
                primary: '#2563eb',
                secondary: '#475569',
                accent: '#f59e0b',
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
    ],
} 