import time
import sys
import math


""" --- I/O FUNCTIONS --- """
# Read test and trainig data and stores in double-keyed (user, item) global dictionary
# Format expected: [user_id]\t[item_id]\t[rating]\t[time_stamp]\n
def read_file(input_data_file, data):

	with open (input_data_file, 'r') as f:
		for line in f.read().split('\n'):
			if line != '':
				# 2-key dictionary
				user_id, item_id, rest = line.split('\t', 2)
				if int(user_id) not in data:
					data[int(user_id)] = {}
				data[int(user_id)][int(item_id)] = int(rest[0])


# Generate output files and write the results
# Output format: [user_id]\t[item_id]\t[rating]\n
def write_file(input_file_name, final_ratings):

	output_file_name = input_file_name + '_prediction.txt'
	with open(output_file_name, 'w') as f:
		for user in final_ratings:
			for item in final_ratings[user].keys():
				f.writelines(str(user) +'\t' + str(item) +'\t' + str(final_ratings[user][item]) +'\n')


""" --- CF FUNCTIONS --- """
# Calculates similarity between two users using Pearson's Correlation Coeficient
# I used the formula in the presentation 
def calculate_similarity(user_a, user_b, common_items):

	# Sum of values
	sum_a = 0
	sum_b = 0
	# Sum of square values
	square_sum_a = 0
	square_sum_b = 0
	# Sum of products
	product_sum = 0

	for item in common_items:
		sum_a += user_a[item]
		sum_b += user_b[item]
		square_sum_a += user_a[item] **2
		square_sum_b += user_b[item] **2
		product_sum += user_a[item] * user_b[item]

	# Denominator
	d = math.sqrt((square_sum_a - (sum_a**2) / len(common_items)) * (square_sum_b - (sum_b**2) / len(common_items)))

	if d == 0:	# Divide by 0, can't happen
		return 0

	else:
		# Numerator
		n = product_sum - (sum_a * sum_b / len(common_items))

		return n/d


# Compares item between two users and returns the common ones
def get_common_items(user_a, user_b):
	
	return (set(user_a.keys())).intersection(set(user_b.keys()))


# Compares the user with the training data and gets a recommended set
def get_recommendations(target_user, user_id, training_data):

	recommendations = {}
	new_items = set()

	for training_user_id in training_data:
		if training_user_id != user_id:	# dont compare with itself
			
			common_items = get_common_items(target_user, training_data[training_user_id])

			# if users have at least 1 item in common, calculate similarity (Pearson's Correlation Coefficient)
			if len(common_items) > 0:
				PCC = calculate_similarity(target_user, training_data[training_user_id], sorted(common_items))

				if PCC > 0:
					for item in training_data[training_user_id]:
						if item not in target_user or target_user[item] == 0:
							recommendations[item] = 0
							recommendations[item] += training_data[training_user_id][item] * PCC

	return recommendations


# 2 arguments expected: training data name, test data name
def main():

	test_data = {}
	training_data = {}
	final_ratings = {}

	training_data_file_name = sys.argv[1]
	test_data_file_name = sys.argv[2]

	# Read files and store data in global dics
	print("Loading data")
	read_file(training_data_file_name, training_data)
	read_file(test_data_file_name, test_data)

	# Recommendations using Collaborative Filtering
	print("Calculating")
	for user_id in test_data:
		recommendations = get_recommendations(test_data[user_id], user_id, training_data)

		if user_id not in final_ratings:
			final_ratings[user_id] = {}
		
		for item in recommendations:
			final_ratings[user_id][item] = recommendations[item]
		
		# Merge recommendations with previous ratings
		final_ratings[user_id].update(test_data[user_id])
	
	# Generate output file
	print("Writing output file")
	write_file(training_data_file_name, final_ratings)
	print("Done")


""" --- TIMER --- """
if __name__ == '__main__':

	startTime = time.time()
	main()
	print("\nExecution time: " +str(round((time.time() - startTime), 4)) +"s\n")