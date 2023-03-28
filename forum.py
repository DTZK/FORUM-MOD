import sys, datetime
	

class User:
	def __init__(self, name: str):
		self.name = name
		self.engagement = 0
		self.expressiveness = 0
		self.offensiveness = 0
	
	def process_message(self, message, banned_words_list: list) -> bool:
		if type(message) != "str":
			return False
		else:
			return True

	def calculate_personality_score(self):
		score = self.expressiveness - self.offensiveness
		rounded_down_score = int(score)
		rounded_down_engagement = int(self.engagement)
		if rounded_down_score > rounded_down_engagement:
			return rounded_down_engagement
		else:
			return rounded_down_score


#list in parameter
def arguements_present(complete_arguement):
	i = 0
	task_arg = 0
	task_index = 0

	log_arg = 0
	log_index = 0

	forum_arg = 0
	forum_index = 0

	words_arg = 0
	words_index =0

	people_arg = 0
	people_index = 0

	#check if arguemnets are present
	while i < len(complete_arguement):
		if complete_arguement[i] == "-task":
			task_arg+=1

		if complete_arguement[i] == "-log":
			log_arg+=1

		if complete_arguement[i] == "-forum":
			forum_arg+=1

		if complete_arguement[i] == "-words":
			words_arg+=1

		if complete_arguement[i] == "-people":
			people_arg+=1
		
		i+=1
	
	#If arguments are not present
	if task_arg!=1:
		print("No task arguments provided.")
		exit()
	
	if log_arg !=1:
		print("No log arguments provided.")
		exit()
	
	if forum_arg != 1:
		print("No forum arguments provided.")
		exit()
	
	if words_arg != 1:
		print("No words arguments provided.")
		exit()
	
	if people_arg != 1:
		print("No people arugments provided.")
		exit()


def argument_check(complete_arguement):
	i = 0
	task_index = 0
	log_file_index = 0
	forum_file_index = 0
	words_file_index = 0
	people_file_index = 0
	
	while i < len(complete_arguement): 
		if complete_arguement[i] == '-task':
			task_index = i +1
			if task_index < len(complete_arguement):
				if not((complete_arguement[task_index] == 'rank_people') or (complete_arguement[task_index] == 'validate_forum') or (complete_arguement[task_index]== 'censor_forum') or (complete_arguement[task_index] == 'evaluate_forum')) == True:
					print("Task argument is invalid.")
					exit()
			else:
				print("Task argument is invalid.")
				exit()

		if complete_arguement[i] == '-log':
			log_file_index = i + 1

		if complete_arguement[i] == '-forum':
			forum_file_index = i + 1
			if forum_file_index < len(complete_arguement):
				file_name = complete_arguement[forum_file_index]
				try:
					open(file_name)
				except Exception:
					print(f"{file_name} cannot be read.")
					exit()
			else:
				print(f"{file_name} cannot be read.")
				exit()

		if complete_arguement[i] == '-words':
			words_file_index = i + 1
			if words_file_index < len(complete_arguement):
				file_name = complete_arguement[words_file_index]
				try:
					open(file_name)
				except Exception:
					print(f"{file_name} cannot be read.")
					exit()
			else:
				print(f"{file_name} cannot be read.")
				exit()	

		if complete_arguement[i] == '-people':
			people_file_index = i +1
			if people_file_index < len(complete_arguement):
				file_name = complete_arguement[people_file_index]
				try:
					open(file_name)
				except Exception:
					print(f"{file_name} cannot be read.")
					exit()
			else:
				print(f"{file_name} cannot be read.")
				exit()
				
		i += 1
	#Returns a tuple to get location of the files
	return (task_index, log_file_index, forum_file_index, words_file_index, people_file_index)


#File header Validation function for people file
def file_header_check(people_file_name, log_file_name):
	with open(people_file_name, 'r') as content:
		lst = content.readlines()

	##Checking if format of entries are correct
	i = 0
	people_entries = []
	if len(lst) == 0:
		with open(log_file_name, 'w') as content:
			content.write("Error: people file read. The people file header is incorrectly formatted\n")
		exit()

	while i < len(lst):
		entry = lst[i]
		entry_lst = entry.split(",")
		if i == 0:
			if len(lst[0]) <= 1 or len(lst) <= 1:
				with open(log_file_name, 'w') as content:
					content.write("Error: people file read. The people file header is incorrectly formatted\n")
				exit()
			
		elif i == 1:	
			if len(lst[1]) != 1:
				with open(log_file_name, 'w') as content:
					content.write('Error: people file read. The people file header is incorrectly formatted\n')
				exit()
		else:
			if len(entry_lst) == 2:
				name = entry_lst[0]
				score = entry_lst[1]
				new_score = score.strip("\n").strip()
				people_entries.append(lst[i])

				if name_check(name) == False:
					with open(log_file_name, 'w') as content:
						content.write(f"Error: people file read. The user's name is invalid on line {i+1}\n")
					exit()

				if score_check(new_score) == False:
					with open(log_file_name, 'w') as content:
						content.write(f"Error: people file read. The personality score is invalid on line {i+1}\n")
					exit()

			else:
				with open(log_file_name, 'w') as content:
					content.write(f'Error: people file read. The people entry is invalid on line {i+1}\n')
				exit()

		i +=1

	w = 0
	#Sort (use reverse) in a descending order
	people_entries.sort(key=descending_sort, reverse= True)
	with open(people_file_name, 'w') as content:
		content.write(f"{lst[0]}")
		content.write(f"{lst[1]}")

	with open(people_file_name, 'a') as content:
		while w < len(people_entries):
			content.write(f"{people_entries[w]}")
			w += 1

	with open(log_file_name, 'w') as content:
		content.write("")				


#Check names
def name_check(name):
	i = 0
	if name.isspace():
		return False

	elif len(name) == 0:
		return False

	elif not isinstance(name, str):
		return False

	while i < len(name):
		if (name[i].isalpha()) or (name[i].isspace()) or (name[i] == "-") == True:
			i += 1
			if i == len(name) - 1:
				return True
		else:
			return False


#Check score between 10 and -10
def score_check(new_score):
	min_score = -10
	max_score = 10
	i = 0
	
	while i < len(new_score):
		if new_score[i].isdigit() or new_score[i] == "-":
			i += 1
		else:
			return False

	if len(new_score) == 0:
		return False

	if min_score <= int(new_score) <= max_score:
		return True
	else:
		return False


#Change elements into an integer data type
def descending_sort(lst):
	 sort_lst= lst.split(',')
	 get_score = sort_lst[1].strip('\n')
	 return int(get_score)


#Part 4
def forum_file_check(forum_file_name):
	with open(forum_file_name, 'r') as content:
		lst = content.readlines()
	#Header check
	try:
		if len(lst) <= 1:
			raise Exception

		elif len(lst[0]) == 0:
			raise Exception
		
		elif len(lst[1]) != 1:
			raise Exception
	except Exception:
		with open(log_file_name, 'w') as content:
			content.write("Error: forum file read. The forum file header is incorrectly formatted\n")
		exit() 

	i = 2
	date_index = 2
	name_index = 3
	while i<len(lst):
		if i == date_index:
			date = lst[i].rstrip()
			if i != 2:
				if post_format(date, lst, i)== False:
					line_error = line_check(date, lst, i)
					with open(log_file_name, 'w') as content:
						content.write(f"Error: forum file read. The post has an invalid format on line {i+1}\n")
					exit()
			
			elif i == 2:
				if date[0] == '\t':
					with open(log_file_name, 'w') as content:
						content.write(f"Error: forum file read. The reply is placed before a post on line {i+1}\n")
					exit()

			date_time = date.strip()
			date_format = "1996-09-12T16:30:16"  
			try:
				#Ensures that it is the right length
				if len(date_time) != len(date_format):
					raise Exception

				#Ensure that dashes are in the right place 
				elif date_time[4] != '-' or date_time[7] != '-':
					raise Exception
				
				#Ensure that T is in the right spot
				elif date_time[10] != 'T':
					raise Exception
				
				#Ensure that : are in the right places
				elif (date_time[13] != ':' or date_time[16] != ':'):
					raise Exception
				#Check if date is valid
				if date_check(date_time) == False:
					raise Exception
				
			except Exception:
				with open(log_file_name, 'w') as content:
					content.write(f"Error: forum file read. The datetime string is invalid on line {i+1}\n")
				exit()
			
			date_index+= 3 

			if i == name_index:
				name = lst[i].strip()
				if name_check(name) == False:
					with open(log_file_name, 'w') as content:
						content.write(f"Error: forum file read. The user's name is invalid on line {i+1}\n") 
					exit()

				name_index+=3
			
		i += 1


#Check dates between the post
def valid_post_date(forum_file_name):
	with open(forum_file_name, 'r') as content:
		lst = content.readlines()

	i = 2
	date_index = 2
	earlier_date = ""
	later_date = ""
	while i<len(lst):
		date = lst[i].rstrip()
		if i == date_index:
			if lst[i] == "\t":
				i+=1 
			#Add the first date in 
			if len(earlier_date) == 0:
				earlier_date = date
			elif len(earlier_date)!= 0 and len(later_date)==0:
				later_date = date
			if len(earlier_date)!= 0 and len(later_date)!=0:
				valid_post_date = is_chronological(earlier_date, later_date)
				if valid_post_date == False:
					return i
			date_index += 3
		i+=1


#Check post format
def post_format(date, lst, i):
	w = i + 3
	if date[0] == '\t':
		while i < w:
			if lst[i][0] != '\t':
				return False
			i+=1
		return True
	
	elif date[0] != '\t':
		while i < w:
			if lst[i][0] == '\t':
				return False
			i+=1
		return True 


#Line format checl
def line_check(date, lst, i):
	w = i + 3
	if date[0] == '\t':
		while i < w:
			if lst[i][0] != '\t':
				return i
			i+=1
		return True
	
	elif date[0] != '\t':
		while i < w:
			if lst[i][0] == '\t':
				return i
			i+=1
		return True


def date_check(date_time):
	i = 0
	dash_count = 0
	t_count = 0
	colon_count = 0
	while i< len(date_time):
		#Check for letters
		if date_time[i].isdigit() or date_time[i] == '-'  or date_time[i]== 'T' or date_time[i]==':':
			if date_time[i] == '-':
				dash_count += 1
			elif date_time[i]== 'T':
				t_count += 1
			elif date_time[i]==':':
				colon_count += 1
			i+= 1
		else:
			return False

	if i == len(date_time) and dash_count == 2 and t_count ==1 and colon_count==2:
		return True


def is_chronological(earlier_date, later_date):
	if earlier_date < later_date:
		return True
	else:
		return False


#Part 4 
def valid_word_file(word_file_name):
	with open(word_file_name, 'r') as content:
		lst = content.readlines()
	#Header validation check of the file
	try:
		if len(lst) <= 1:
			raise Exception

		elif len(lst[0]) == 0:
			raise Exception
		
		elif len(lst[1]) != 1:
			raise Exception

	except Exception:
		with open(log_file_name, 'w') as content:
			content.write("Error: words file read. The words file header is incorrectly formatted\n")
		exit()
	
	i = 2
	banned_words = []
	while i < len(lst):
		#Checking of banned words
		current_word = lst[i]
		if ban_word_check(current_word) == False:
			with open(log_file_name, 'w') as content:
				content.write(f"Error: words file read. The banned word is invalid on line {i+1}\n")
			exit()
		else:
			banned_words.append(lst[i])
		i+=1

	return banned_words


def ban_word_check(current_word):
	w = 0
	banned_characters = [" ", "\n", "\t", ",",".", "'", "\"", "!", "?", "(", ")" ]
	while w < len(banned_characters):
		#check if starting character is a banned word
		if current_word[0] == banned_characters[w]: 
			count = 0
			#Check if ending character is a banned word if starting has a banned word
			while count < len(banned_characters):
				if current_word[-1] == banned_characters[count]:
					return False
				count+=1
		w+=1


#Part 5
def forum_censor(forum_file_name, banned_words_list):
	with open(forum_file_name, 'r') as content:
		lst = content.readlines()

	i = 4
	while i<len(lst):
		string = lst[i]
		w = 0
		while w < len(banned_words_list):
			word = banned_words_list[w][:-1]
			illegal_word_index = string.find(banned_words_list[w][:-1])
			if illegal_word_index != -1:
				p = illegal_word_index
				#check if the starting letter and ending letter of the word the same
				if p==0 and string(p+len(word).isalpha()==False):
					lst[i] = lst[i].replace(word, "*"*len(word))
				elif (string[p-1].isalpha() or string[p+len(word)].isalpha())== False:
					lst[i] = lst[i].replace(word, "*"*len(word))
			w+=1
		i+= 3
	
	clear_document = open(forum_file_name, 'w')
	clear_document.close()

	i = 0
	while i< len(lst):
		with open(forum_file_name, 'a') as content:
			content.write(f"{lst[i]}")
		i+=1


if __name__== "__main__" :
	#Placing the whole command line argument into a string separated with ,
	sentence_arguement = ','.join(sys.argv)
	#COnverting the string into a list
	complete_arguement = sys.argv #list
	arguements_present(complete_arguement)

	file_location = argument_check(complete_arguement)
	#tuple (task_index, log_file_index, forum_file_index, words_file_index, people_file_index)

	print("Moderator program starting...")
	
	# Location of people file
	people_file_index = file_location[4]

	#Getting the name for people file
	people_file_name = complete_arguement[people_file_index]
	
	#Getting the location of log file
	log_file_index = file_location[1]

	#Getting the name for the log file
	log_file_name = complete_arguement[log_file_index]
	
	#file header validation
	file_header_check(people_file_name, log_file_name)

	#Part 4
	forum_file_index = file_location[2]
	forum_file_name = complete_arguement[forum_file_index]

	forum_file_check(forum_file_name)
	posts_ordered = valid_post_date(forum_file_name)
	
	#Check valid words file
	word_file_index = file_location[3]
	word_file_name = complete_arguement[word_file_index]
	#Receives the banned words
	banned_words_list = valid_word_file(word_file_name)

	forum_censor(forum_file_name, banned_words_list)
	
