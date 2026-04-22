from pathlib import Path
path = Path('cultural_advisor/advisor/views.py')
text = path.read_text(encoding='utf-8')
start = text.find('# ---------------------------\n# MAIN CHATBOT LOGIC\n')
end = text.find('# HISTORY VIEWS (Remained same)\n', start)
if start == -1 or end == -1:
    raise SystemExit('Could not locate duplicate chatbot block')
new_text = text[:start] + '# HISTORY VIEWS (Remained same)\n' + text[end + len('# HISTORY VIEWS (Remained same)\n'):]
path.write_text(new_text, encoding='utf-8')
print('removed duplicate block')
