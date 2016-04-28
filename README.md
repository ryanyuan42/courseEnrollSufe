# courseEnrollSufe

Hi, this project is mainly aiming at helping SUFE students get enrolled.

This is a unfinished project with a lot of places to modify. It requires:
 * ```requests```
 * ```bs4```

If you are interested, you can clone the project and test it and modify it.

Currently, it will send msg to your email address if anything happened. I don't think it helps any though...

Usage:

```python course_enrollment.py```

This project act as a web crawler to keep sending enroll request to the server if it discvoer there is an extra spot.(The part I didn't write yet)


#### There are two problems in this project,
 * It has to be opened all the time by your computer. (I am thinking about using cloud platform? make it a web app?)
 * It can not get the neccessary information to enroll in a class automatically. Still it requies human work.(for the course id and v)

#### missing part:

For getting enrolled in a course, there are two strategies:
 * One, waiting the course to be released and be the first one to get enrolled, which is what I've already realized.
 * Two, cannot get enrolled right now, so wait until there are more room in this course and be the first one to get enrolled.
 * The second strategy is not realized yet.
 * But I think it's pretty simple and can be done in a few codes.

First, get the id of a course, which can be something you feed in the program

Second, use crawler to get the limit students number(ln) and current students number(cn) of the course.

Third, if ln > cn, enroll in it.

Fourth, if not, return to second step.


