from unittest import TestCase
from scheduler import Scheduler, Course
import os
import json


class TestScheduler(TestCase):

    def test_customer_json_file(self):
        mock_file = None
        try:
            # creating a mock json file and read it
            mock_file = open('mock_courses.json', 'w')
            json.dump([{"name": "Calculus"}], mock_file)
            mock_file.close()
            mock_json = Scheduler('mock_courses.json').read_customer_json_file()
            self.assertEqual(mock_json[0]['name'], 'Calculus')
        except IOError:
            raise Exception('Error: Could not create mock file')
        finally:
            if mock_file:
                mock_file.close()
                os.remove('mock_courses.json')

    def test_get_course_list(self):
        mock_courses = [
         {
            "name": "Relativity",
            "prerequisites": ["Calculus"]
        },
        {
            "name": "Calculus",
            "prerequisites": []
        }
         ]
        course_list = Scheduler('mock_courses.json').get_course_list(mock_courses)
        self.assertEqual(len(course_list), 2)
        self.assertEqual(course_list[0].name, 'Relativity')

    def test_course_with_circular_dependency(self):
        mock_courses = [
         {
            "name": "Relativity",
            "prerequisites": ["Differential Equations", "Intro to Physics"]
        },
        {
            "name": "Calculus",
            "prerequisites": []
        }
         ]
        self.assertRaises(SystemExit, lambda:Scheduler('mock_courses.json').get_course_list(mock_courses))

        # A->B, B->C, C->A.
        algebra = Course('algebra')
        geometry = Course('geometry')
        physics = Course('physics')
        algebra.add_prerequisite_courses(geometry)
        geometry.add_prerequisite_courses(physics)
        physics.add_prerequisite_courses(algebra)

        self.assertRaises(SystemExit, lambda:Scheduler('mock_courses.json').get_ordered_courses([algebra, physics,
                                                                                                 geometry]))

    def test_course_list_with_self_dependency(self):
        mock_courses = [
        {
            "name": "Calculus",
            "prerequisites": ["Calculus"]
        }
         ]
        self.assertRaises(SystemExit, lambda:Scheduler('mock_courses.json').get_course_list(mock_courses))

    def test_course_list_with_missing_prerequisite_course(self):
        mock_courses = [
        {
            "name": "Relativity",
            "prerequisites": ["Calculus"]
        }
         ]
        self.assertRaises(SystemExit, lambda:Scheduler('mock_courses.json').get_course_list(mock_courses))

    def test_get_ordered_courses(self):
        # test single dependency
        algebra = Course('algebra')
        algebra_a = Course('algebra_a')
        algebra_a.add_prerequisite_courses(algebra)

        ordered_courses = Scheduler('mock_courses.json').get_ordered_courses([algebra_a, algebra])
        self.assertEqual(len(ordered_courses), 2)
        self.assertEqual(ordered_courses[0].name, 'Algebra')

        # test multiple dependencies
        geometry = Course('geometry')
        physics = Course('physics')
        physics.add_prerequisite_courses(algebra)
        physics.add_prerequisite_courses(geometry)

        ordered_courses = Scheduler('mock_courses.json').get_ordered_courses([physics, algebra, geometry])
        self.assertEqual(len(ordered_courses), 3)
        self.assertEqual(ordered_courses[2].name, 'Physics')


    def test_traverse_course_dependencies(self):
        geometry = Course('geometry')
        physics = Course('physics')
        algebra = Course('algebra')
        physics.add_prerequisite_courses(algebra)
        physics.add_prerequisite_courses(geometry)

        scheduler = Scheduler('mock_courses.json')
        scheduler.traverse_course_dependencies(physics)

        self.assertEqual(len(scheduler.ordered_course_list), 3)
        self.assertEqual(scheduler.ordered_course_list[2].name, 'Physics')
