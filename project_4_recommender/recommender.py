import time
import sys
import math

# Global variable storing the data
test_data = {}
training_data = {}

final_recommendations = {}


""" --- I/O FUNCTIONS --- """
# Read test and trainig data and stores in double-keyed (user, item) global dictionary
# Format expected: [user_id]\t[item_id]\t[rating]\t[time_stamp]\n
def read_file(input_data_file, data):

	with open (input_data_file, 'r') as f:
		for line in f.read().split('\n'):
			if line != '':
				"""
				# Dictionary with list of items, values and timestamp
				user_id, rest = line.split('\t', 1)
				if int(user_id) not in data:
					data[int(user_id)] = list()
				data[int(user_id)].append([int(value) for value in rest.split()])
				"""
				# 2-key dictionary
				user_id, item_id, rest = line.split('\t', 2)
				if int(user_id) not in data:
					data[int(user_id)] = {}
				data[int(user_id)][int(item_id)] = int(rest[0])


# Generate output files and write the results
def write_file(input_file_name):

	global final_recommendations

	output_file_name = input_file_name + '_prediction.txt'
	with open(output_file_name, 'w') as f:
		for user in final_recommendations:
			for item in final_recommendations[user].keys():
				f.writelines(str(user) +'\t' + str(item) +'\t' + str(final_recommendations[user][item]) +'\n')


""" --- HELPER FUNCTIONS --- """


""" --- CF FUNCTIONS --- """
# Calculates similarity between two users using Pearson's Correlation Coeficient
# I simplified the covariance and std_deviation formulas by extracting the 1/(n-1)
def calculate_similarity(user_a, user_b, common_items):

	
	denominator = math.sqrt(std_deviation(user_a, common_items) * std_deviation(user_b, common_items))
	if denominator == 0:
		return -1
	else:
		return (covariance(user_a, user_b, common_items) / denominator)
	

	 
# Covariance without 1/(1-n)
def covariance(user_a, user_b, common_items):

	values_a = []
	values_b = []

	for item in common_items:
		values_a.append(user_a[item])
		values_b.append(user_b[item])

	mean_a = sum(values_a) / len(values_a)
	mean_b = sum(values_b) / len(values_b)

	cov = 0

	for i in range(len(common_items)):
		cov += ((values_a[i] - mean_a) * (values_b[i] - mean_b))

	return cov


# Standard deviation without 1/(1-n)
def std_deviation(user, items):

	values = []
	for item in sorted(items):
		values.append(user[int(item)])

	mean = sum(values) / len(values)

	std_dev = 0

	for i in range(len(values)):
		std_dev += (values[i] - mean)**2

	return std_dev


# Calculates average rating given by one user
def get_average(user):

	addition = 0

	for item in user.keys():
		addition += user[item]
	
	return addition / len(user)


# Compares item between two users and returns the common ones
def get_common_items(user_a, user_b):
	
	return (set(user_a.keys())).intersection(set(user_b.keys()))


# Aggregation (following formula in the presentation)
def aggregate(user_id, recommendations, new_items):

	global test_data
	global training_data
	global final_recommendations

	user_average = get_average(test_data[user_id])

	if user_id not in final_recommendations:
			final_recommendations[user_id] = {}

	for item in new_items:

		neighbour_added_rating = 0
		k = 0
		for recommendation in recommendations:
			if item in recommendation[2]:	#dictionary
				neighbour_added_rating += (recommendation[1] * (recommendation[2][item] - get_average(training_data[recommendation[0]])))
				k += 1	

		final_recommendations[user_id][item] = user_average + (1/k)*neighbour_added_rating


# Compares the user with the training data and gets a recommended set
def get_recommendations(target_user, user_id, training_data):

	user_recommendations = []
	new_items = set()

	for training_user_id in training_data:
		if training_user_id != user_id:	
			
			common_items = get_common_items(target_user, training_data[training_user_id])

			if len(common_items) > 0:
				pcc = calculate_similarity(target_user, training_data[training_user_id], sorted(common_items))

				if pcc > 0:
					item_ratings = {}
					different_items = set(training_data[training_user_id].keys()).difference(sorted(common_items))
						
					for item in sorted(different_items):
						new_items.add(item)
						item_ratings[item] = training_data[training_user_id][item]

					# Save training_user_id, pcc, ratings for each item (dict)
					user_recommendations.append([training_user_id, pcc, item_ratings])

	# Once we have pcc and ratings, aggregate
	aggregate(user_id, user_recommendations, sorted(new_item_recommendation))


# Adds test data to results
def merge_results():
	global test_data
	global final_recommendations

	for user in test_data:
		final_recommendations[user].update(test_data[user])


# 2 arguments expected: training data name, test data name
def main():

	training_data = {}
	test_data = {}

	training_data_file_name = sys.argv[1]
	test_data_file_name = sys.argv[2]

	# Read files and store data in global dics
	print("Loading data")
	read_file(training_data_file_name, training_data)
	read_file(test_data_file_name, test_data)

	print("Calculating")
	# Recommendations using Collaborative Filtering
	for user_id in test_data:
		get_recommendations(test_data[user_id], user_id, training_data)

	print("Merging")
	# Merge dictionaries
	# merge_results()

	# Generate output file
	print("Writing output file")
	write_file(training_data_file_name)

	print("Done")


""" --- TIMER --- """
if __name__ == '__main__':

	startTime = time.time()
	main()
	print("\nExecution time: %ss\n" % (time.time() - startTime))