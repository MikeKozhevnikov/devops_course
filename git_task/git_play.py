import requests
import re
import sys

def check_req(url, params):
	check = requests.get(url, params)
	if check.status_code != 200:
		print('Error in user name or user repo')
		quit()
	return check

### Open pulls in repo
def get_open_pulls(user, repo):
	params = {'per_page' : 100, 'state':'open'}
	req_reps_names = check_req(f"https://api.github.com/repos/{user}/{repo}/pulls", params)
	print("\nOpen pull requests:")
	for i in req_reps_names.json():
		print(f"\nTitle: \"{i['title']}\"\nUser: \"{i['user']['login']}\"")



### Most popular authors
def get_most_prod_authors(user, repo):
	dict_authors = {}
	for i in range(1, 6):
		params = {'per_page' : 100, 'page' : i, 'state': 'all'}
		req_reps_pulls = check_req(f"https://api.github.com/repos/{user}/{repo}/pulls", params)
		
		for i in req_reps_pulls.json():
			name = i['user']['login']
			count_pr = dict_authors.get(name, {}).get('Number of PR', 0) + 1
			dict_authors[name] = {'Number of PR':count_pr}

	dict_authors = [(key, value) for key, value in dict_authors.items() if value['Number of PR'] > 1]
	dict_authors.sort(key=lambda i: i[1]['Number of PR'], reverse=True)
	dict_authors = dict(dict_authors)
	print("\nMost popular authors:")
	for key, value in dict_authors.items():
		print(f"\nAuthor: {key}\nThe number of PR: {value['Number of PR']}")




### The number of PR each contributors witch labels
def get_all(user, repo):
	dict_authors = {}
	for i in range(1, 6):
		params = {'per_page' : 100, 'page' : i, 'state': 'all'}
		req_reps_pulls = check_req(f"https://api.github.com/repos/{user}/{repo}/pulls", params)

		for i in req_reps_pulls.json():
			name = i['user']['login']
			labels =  dict_authors.get(name, {}).get('Labels', []) + [i['name'] for i in i['labels'] if i]
			count_pr = dict_authors.get(name, {}).get('Number of PR', 0) + 1
			dict_authors[name] = {'Number of PR':count_pr, 'Labels':list(set(labels))}

	dict_authors = [(key, value) for key, value in dict_authors.items() if value['Number of PR'] > 1]
	dict_authors.sort(key=lambda i: i[1]['Number of PR'], reverse=True)
	dict_authors = dict(dict_authors)
	print("\nPull requests with contributors and labels:")
	for key, value in dict_authors.items():
		print(f"\nAuthor: {key}\nThe number of PR: {value['Number of PR']}\nLabels: {value['Labels']}")


### Show commits since a specific date
def get_commits(user, repo):
	date = input('Date format YYYY-MM-DDTHH:MM:SSZ): ')
	params = {'per_page' : 100, 'since':date}
	dict_commits = {}
	req_reps_commits = check_req(f"https://api.github.com/repos/{user}/{repo}/commits", params)
	print(f"\nCommits since {date}:")
	for i in req_reps_commits.json():
		print(f"\nAuthor: {i['commit']['author']['name']}\nMessage: {i['commit']['message']}\n\n")





opt_dict = {'1':get_open_pulls, '2':get_most_prod_authors, '3':get_all, '4':get_commits}

### Menu
def choice_func():
	message = '''1) Show open pull requests
2) Show most productive contributors
3) Show pull requests with contributor and labels
4) Show commits since a specific date'''
	choice = input(f'{message}\nEnter the number from 1 to {len(opt_dict)}: ')
	match = re.search(r'[1-4]', choice)
	if match:
		opt_dict[choice](user_name, user_repo)
	else:
		print('Only a digit from 1 to 3')


#templ="https://github.com/freeCodeCamp/freeCodeCamp/asdasd/as/aas"

###Check key
if len(sys.argv) >= 3:
	if sys.argv[1] == "-u" or sys.argv[1] == "--url":
		try:
			regex=(r'github.com/(?P<user>[\w\-.]+)/(?P<repo>[\w\-.]+)')
			url_match = re.search(regex, sys.argv[2])
			user_name = url_match.group('user')
			user_repo = url_match.group('repo')
			choice_func()
		except:
			print(f"Wrong url: '{sys.argv[2]}'\nUse '-u' if you want to pass a link.\nExample: git_play.py -u https://github.com/user/repo")
	else:
		print(f"Wrong key: '{sys.argv[1]}'\nUse '-u'' if you want to pass a link.\nExample: git_play.py -u https://github.com/user/repo")
		quit()
else:
	user_name = input('User git username: ')
	user_repo = input('User git repository: ')
	choice_func()

