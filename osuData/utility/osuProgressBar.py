"""To display a basic progress bar and info."""

import sys


def progress_bar(iteration, total, start=0, info='', suffix='', length=75, fill='█'):
	del_last_line = '\x1b[1A\x1b[2K'
	if iteration > start:
		sys.stdout.write(del_last_line*2 if info == '' else del_last_line*2)

	percent = str(round(100*(iteration+1)/total, ndigits=3))
	filled_length = int(length * (iteration+1) // total)
	bar = fill * filled_length + ' ' * (length - filled_length)

	if info.strip() != '':
		print(info)

	sys.stdout.write(f'\n{percent}% |{bar}| {iteration+1}/{total} {suffix}\n')
