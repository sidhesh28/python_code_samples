import json
import sys
import argparse

''' Course object
    Properties:
    name: str
    prerequisite_courses: list of Course objects
'''
class Course(object):
    def __init__(self, name):
        self.name = name.title()
        self.prerequisite_courses = []

    def add_prerequisite_courses(self, prerequisite_course):
        # check if prerequisite_course is Course object
        if not type(prerequisite_course) == Course:
            print('Error: Prerequisite_course should be of type Course', file=sys.stderr)
            sys.exit(1)
        # avoid duplicates
        elif prerequisite_course in self.prerequisite_courses:
            return

        else:
            self.prerequisite_courses.append(prerequisite_course)

''' Reads list of courses and their prerequisite courses from and json file
    and prints a valid ordering of classes.
'''
class Scheduler():

    def __init__(self, courses_json_file_path):
        self.courses_json_file_path = courses_json_file_path
        # stores ordered list of courses
        self.ordered_course_list = []
        # keeping track of start node while traversing to detect circular dependencies.
        self._current_start_course = None

    ''' Creates list of Course objects from input json file
        and prints a valid ordering of classes.
    '''
    def execute(self):
        courses_dict = self.read_customer_json_file()
        course_list = self.get_course_list(courses_dict)
        ordered_course_list = self.get_ordered_courses(course_list)
        self.print_ordered_courses(ordered_course_list)


    ''' Read courses json file and return courses dict.
    '''
    def read_customer_json_file(self):
        courses_json_file = None
        courses_dict = {}

        try:
            courses_json_file = open(self.courses_json_file_path)
            courses_dict = json.load(courses_json_file)
        except IOError:
            print('Error: Could not open file {}'.format(self.courses_json_file_path), file=sys.stderr)
            sys.exit(1)
        except Exception:
            print('Error: Could not parse input json', file=sys.stderr)
            sys.exit(1)
        finally:
            if courses_json_file:
                courses_json_file.close()

        return courses_dict

    ''' Returns a list of Course objects offered
    '''
    def get_course_list(self, courses_dict):
        course_list = []
        course_obj_map = {}

        # create map of course obj offered
        for course in courses_dict:
            try:
                if course == '':
                    print('Error: Empty string found in course name', file=sys.stderr)
                    sys.exit(1)
                course_obj_map[course['name']] = Course(name=course['name'])
            except KeyError:
                print("Error: Missing key 'name' in input json", file=sys.stderr)
                sys.exit(1)

        # read prerequisite courses for every course from courses_json,
        # validate prerequisite courses in json,
        # add prerequisities for each course and add course obj to course_list
        for course in courses_dict:
            try:
                course_obj = course_obj_map[course['name']]
                for prerequisite_course in course['prerequisites']:
                    if self.validate_prerequisite_course(course_obj, course_obj_map, prerequisite_course):
                        course_obj.add_prerequisite_courses(course_obj_map[prerequisite_course])
            except KeyError:
                print("Error: Missing key 'prerequisites' in input json", file=sys.stderr)
                sys.exit(1)
            course_list.append(course_obj)

        return course_list

    ''' Validate prerequisite_course for a course object
    '''
    @classmethod
    def validate_prerequisite_course(cls, course, all_courses_map, prerequisite_course):
            if prerequisite_course == '':
               print("Error: Empty string found in prerequisite_course 'name'", file=sys.stderr)
               sys.exit(1)
            # check if the prerequisite course is being offered
            if prerequisite_course not in all_courses_map.keys():
                print('Error: Prerequisite course {} not in courses offered list'.format(prerequisite_course),
                      file=sys.stderr)
                sys.exit(1)
            # check for self-dependency
            if prerequisite_course == course.name:
                print('Error: Course {} has itself as a prerequisite course'.format(course.name), file=sys.stderr)
                sys.exit(1)
            # check for circular dependency
            if course in all_courses_map[prerequisite_course].prerequisite_courses:
                print('Error: Circular dependency - {} & {} are prerequisite_courses for each other'.format(
                        course.name, prerequisite_course), file=sys.stderr)
                sys.exit(1)
            return True

    ''' Return a list of ordered course from all courses list
    '''
    def get_ordered_courses(self, course_list):
         # clearing ordered courses list
        self.ordered_course_list = []
        self._current_start_course = None

        for course in course_list:
            self._current_start_course = course
            self.traverse_course_dependencies(course)
        return self.ordered_course_list

    ''' Traverses course dependencies in depth-first manner and adds Course objects to
        ordered_course_list
    '''
    def traverse_course_dependencies(self, course):
        if course in self.ordered_course_list:
            return
        for pc in course.prerequisite_courses:
            if pc not in self.ordered_course_list:
                if pc == self._current_start_course:
                    print("Error:Circular dependency found for {}".format(self._current_start_course.name),
                          file=sys.stderr)
                    sys.exit(1)
                else:
                    self.traverse_course_dependencies(pc)
        self.ordered_course_list.append(course)

    ''' Display ordered list of courses.
    '''
    @classmethod
    def print_ordered_courses(cls, ordered_course_list):
        for course in ordered_course_list:
            print(course.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("courses_json_file", help="customer json file path")
    args = parser.parse_args()

    Scheduler(args.courses_json_file).execute()



if __name__ == "__main__":
    main()