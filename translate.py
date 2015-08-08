f_out = open('out.txt', 'w+')

def translate_fun(orig_text, translated_text):
	orig_tokens = orig_text.split('.')
	translated_tokens = translated_text.split('.')
	for i in range(0, min(len(orig_tokens), len(translated_tokens))):
		#f_out.write(orig_tokens[i])
		print(i)
		f_out.write(translated_tokens[i])
		#f_out.write(str(i)+'\n')

f1 = open('CHAPTER I. Down the Rabbit-Hole.txt', encoding='utf-8')
f2 = open('Глава I. ВНИЗ ПО КРОЛИЧЬЕЙ HOPE.txt', encoding='utf-8')

translate_fun(f1.read(), f2.read())