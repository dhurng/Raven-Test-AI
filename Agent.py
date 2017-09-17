# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass


    def Solve(self,problem):
        ab_sum = 0
        ac_sum = 0

        solution = -1

        if problem.problemType == '2x2':
            for fig in problem.figures:
                # iter through figures
                curr_fig = problem.figures[fig]
                if curr_fig.name == 'A':
                    continue
                elif curr_fig.name == 'B':
                    ab_sum = self.compare(problem.figures['A'], problem.figures['B'])

                elif curr_fig.name == 'C':
                    ac_sum = self.compare(problem.figures['A'], problem.figures['C'])
                else:
                    b_sol_sum = self.compare(problem.figures['B'], curr_fig)
                    c_sol_sum = self.compare(problem.figures['C'], curr_fig)

                    if ab_sum == c_sol_sum and ac_sum == b_sol_sum:
                        solution = curr_fig

                    # at the end of all options, means that there are diff attr, just generate
                    elif (ab_sum != c_sol_sum or ac_sum != b_sol_sum) and curr_fig.name == '6' and isinstance(solution, (int, long)):
                        return self.generate(problem.figures['B'], problem.figures['C'], curr_fig)

            if not isinstance(solution, (int, long)):
                return int(solution.name)
            else:
                return solution

        if problem.problemType == '3x3':
            return -1

    def generate(self, fig_b, fig_c, curr_fig):
        # compare the generate with the curr_fig

        return -1


    def compare_2(self, fig_1, fig_2):
        weight_table = dict()

        transform_map = dict()

        f1_obj_map = dict()
        f2_obj_map = dict()

        # can zip if needed
        for object_name in fig_1.objects:
            curr_obj = fig_1.objects[object_name]
            if curr_obj not in f1_obj_map:
                f1_obj_map[curr_obj] = []

        for object_name2 in fig_2.objects:
            curr_obj2 = fig_2.objects[object_name2]
            if curr_obj2 not in f2_obj_map:
                f2_obj_map[curr_obj2] = []

    #     not 2 maps of all the objects from each figure
    #             for every object in f1 check if there is an obj f2 that is closely related
        for f1_obj in f1_obj_map:
            for f2_obj in f2_obj_map:
                weight = 1
                for attr_name in f1_obj.attributes:
                    attr_value_f1 = f1_obj.attributes[attr_name]

                    # add to weight table to judge the attributes and give them weight
                    if attr_name not in weight_table:
                        weight_table[attr_name] = [weight]
                        # increment to give it a weight
                        weight += 1

                    # just skip this attribute then but have it in weight table
                    if attr_name not in f2_obj.attributes:
                        break

                    attr_value_f2 = f2_obj.attributes[attr_name]
                    if attr_value_f1 == attr_value_f2:
                        transform_map[attr_name] = 0
                    else:
                        # right now just add the 2 values that are diff
                        transform_map[attr_name] = (attr_value_f1, attr_value_f2, weight_table[attr_name])
                        # transform_map[attr_name] = weight_table[attr_name]

            # go through all corresponding obj 2 and check weight
            for check_f2_obj in f1_obj_map[f1_obj]:


                f1_obj_map[f1_obj].append((f2_obj, ))
    #        now that all objs in f2 are in an object of 1, try to associate with closest weight



    def compare(self, figure1, figure2):
        # reversed for higher weight with more change
        weight_table = {'unchanged' : 0,
                        'reflected' : 1,
                        'rotated': 2,
                        'scaled': 3,
                        'deleted': 4,
                        'shape_changed': 5}

        f1_map = dict()
        f2_map = dict()

        for obj in figure1.objects:
            curr_obj = figure1.objects[obj]
            f1_map[curr_obj] = []

        for obj2 in figure2.objects:
            curr_obj2 = figure2.objects[obj2]
            f2_map[curr_obj2] = []

        # go through the stored objects
        for f1_obj in f1_map:
            for f2_obj in f2_map:
                weight = 0
        #         go thru attr of the obj and compare
                for attr_name in f1_obj.attributes:
                    attr_val = f1_obj.attributes[attr_name]
                    if attr_name in f2_obj.attributes:
                        # here we can give individual weights
                        if attr_val == f2_obj.attributes[attr_name]:
                            continue
                        # not the same values so giv special weight
                        else:
                            if attr_name == 'shape':
                                weight += weight_table['shape_changed']
                            #     dont know what to consider this as
                            elif attr_name == 'fill':
                                weight += 1
                            elif attr_name == 'angle':
                                diff = abs(int(attr_val) - int(f2_obj.attributes[attr_name]))
                                if diff == 90 or diff == 180 or diff == 270 or diff == 360:
                                    weight += weight_table['reflected']
                                else:
                                    weight += weight_table['rotated']
                            elif attr_name == 'size':
                            #     does it have to be same shape before?
                                weight += weight_table['scaled']
                            # elif attr_name == 'alignment':
                            #     pass
                            #     take the C object, use the same left all attribute, and opposite of B attr
                            else:
                                # this would be a very different attribute, probably diff object relationship?
                                weight += 6
                    # if attribute isnt the same
                    else:
                        continue
                #     how to consider deleted?
                f1_map[f1_obj].append((f2_obj, weight))
        total_weight = 0
        for k, v in f1_map.iteritems():
            for target in v:
                total_weight += target[1]
        return total_weight
