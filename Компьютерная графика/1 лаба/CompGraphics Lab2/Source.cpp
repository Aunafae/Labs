// X - красный
// Y - зелёный
// Z - синий

#include <glut.h>
#include <math.h>

int left_and_right = 0;
int up_and_down = 0;
float baseRadius = 0.38;
float carrotRadius = 0.03;
float carrotHeight = 0.2;
float headCoefficient = 0.37;
float eyeCoefficient = 0.07;
float childScale = 0.7;
int task = 1;

void specialkeys(int key, int x, int y) {
	if (key == GLUT_KEY_F1) {
		if (task - 1 < 1) task = 12;
		else task -= 1;
		left_and_right = 0;
		up_and_down = 0;
	}
	if (key == GLUT_KEY_F2) {
		if (task + 1 > 12) task = 1;
		else task += 1;
		left_and_right = 0;
		up_and_down = 0;
	}
	if (key == GLUT_KEY_LEFT) left_and_right -= 2;
	if (key == GLUT_KEY_RIGHT) left_and_right += + 2;
	if (key == GLUT_KEY_UP) up_and_down -= 2;
	if (key == GLUT_KEY_DOWN) up_and_down += 2;
	up_and_down = (up_and_down+360) % 360;
	left_and_right = (left_and_right+360) % 360;
	glutPostRedisplay();
}

void Axes() {
	glBegin(GL_LINES);
	glColor3f(1, 0, 0);
	glVertex3f(0, 0, 0);
	glVertex3f(1, 0, 0);

	glColor3f(0, 1, 0);
	glVertex3f(0, 0, 0);
	glVertex3f(0, 1, 0);

	glColor3f(0, 0, 1);
	glVertex3f(0, 0, 0);
	glVertex3f(0, 0, 1);

	glEnd();
}

void drawSnowMan() {
	Axes();
	// тело снеговика
	glColor3f(1, 1, 1);
	glPushMatrix();
	glutSolidSphere(baseRadius, 20, 20);
	// голова снеговика
	glTranslatef(0, baseRadius+baseRadius*headCoefficient, 0);
	glPushMatrix();
	glScalef(headCoefficient, headCoefficient, headCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	// глаза
	glColor3f(0, 0, 0);
	glPushMatrix();
	glRotatef(30, 0, 1, 0);
	glTranslatef(0, baseRadius * eyeCoefficient, baseRadius*headCoefficient);
	glScalef(eyeCoefficient, eyeCoefficient, eyeCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	glPushMatrix();
	glRotatef(-30, 0, 1, 0);
	glTranslatef(0, baseRadius * eyeCoefficient, baseRadius * headCoefficient);
	glScalef(eyeCoefficient, eyeCoefficient, eyeCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	// нос
	glColor3f(1, 0.4, 0);
	glTranslatef(0, 0, baseRadius * headCoefficient);
	glutSolidCone(carrotRadius, carrotHeight, 20, 20);
	glPopMatrix();
}

void task1() {
	Axes();
	// тело снеговика
	glColor3f(1, 1, 1);
	glPushMatrix();
	glTranslatef(0, baseRadius, 0);
	glutSolidSphere(baseRadius, 20, 20);
	// голова снеговика
	glTranslatef(baseRadius + baseRadius * headCoefficient, -baseRadius + baseRadius * headCoefficient, 0);
	glPushMatrix();
	glScalef(headCoefficient, headCoefficient, headCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	// глаза
	glColor3f(0, 0, 0);
	glTranslatef(baseRadius * headCoefficient + baseRadius * eyeCoefficient, -baseRadius * headCoefficient + baseRadius * eyeCoefficient, 0);
	glPushMatrix();
	glScalef(eyeCoefficient, eyeCoefficient, eyeCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	glTranslatef(baseRadius * eyeCoefficient * 3, 0, 0);
	glPushMatrix();
	glScalef(eyeCoefficient, eyeCoefficient, eyeCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	// нос
	glColor3f(1, 0.4, 0);
	glTranslatef(baseRadius * eyeCoefficient * 4, -baseRadius * eyeCoefficient, 0);
	glRotatef(-90, 1, 0, 0);
	glutSolidCone(carrotRadius, carrotHeight, 20, 20);
	glPopMatrix();
}

void task2() {
	glRotatef(left_and_right, 0, 1, 0);
	drawSnowMan();
}

void task3() {
	glRotatef(left_and_right, 0, 1, 0);
	drawSnowMan();
	glTranslatef(baseRadius + baseRadius*childScale, 0, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
	glTranslatef(baseRadius + baseRadius * childScale, 0, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
}

void task4() {
	drawSnowMan();
	glPushMatrix();
	glTranslatef(0, baseRadius * childScale + baseRadius * childScale * headCoefficient, 0);
	glRotatef(left_and_right, 0, 0, 1);
	glTranslatef(0, -(baseRadius * childScale + baseRadius * childScale * headCoefficient), 0);
	glTranslatef(0, 0, baseRadius + baseRadius * childScale);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
	glPopMatrix();
	glTranslatef(0, 0, baseRadius + baseRadius * childScale * 2 + baseRadius * childScale * childScale);
	glScalef(childScale * childScale, childScale * childScale, childScale * childScale);
	drawSnowMan();
}

void task5() {
	glRotatef(left_and_right, 0, 1, 0);
	drawSnowMan();
	glTranslatef(0, baseRadius + baseRadius * headCoefficient * 2 + baseRadius * childScale, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
	glTranslatef(0, baseRadius + baseRadius * headCoefficient * 2 + baseRadius * childScale, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
}

void task6() {
	glRotatef(left_and_right, 0, 1, 0);
	glRotatef(up_and_down, 1, 1, 1);
	drawSnowMan();
	glRotatef(-up_and_down, 1, 1, 1);
	glRotatef(45, 0, 0, 1);
	glRotatef(-45, 0, 1, 0);
	glTranslatef(baseRadius + baseRadius * childScale, 0, 0);
	glRotatef(45, 0, 1, 0);
	glRotatef(-45, 0, 0, 1);
	glScalef(childScale, childScale, childScale);
	glRotatef(up_and_down, 1, 1, 1);
	drawSnowMan();
	glRotatef(-up_and_down, 1, 1, 1);
	glRotatef(45, 0, 0, 1);
	glRotatef(-45, 0, 1, 0);
	glTranslatef(baseRadius + baseRadius * childScale, 0, 0);
	glRotatef(45, 0, 1, 0);
	glRotatef(-45, 0, 0, 1);
	glScalef(childScale, childScale, childScale);
	glRotatef(up_and_down, 1, 1, 1);
	drawSnowMan();
}

void task7() {
	glTranslatef(baseRadius + baseRadius * childScale, 0, 0);
	glRotatef(left_and_right, 0, 1, 0);
	glTranslatef(-(baseRadius + baseRadius * childScale), 0, 0);
	glTranslatef(0, baseRadius, 0);	
	drawSnowMan();
	glTranslatef(baseRadius + baseRadius * childScale, -baseRadius + baseRadius * childScale, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
	glTranslatef(baseRadius + baseRadius * childScale, -baseRadius + baseRadius * childScale, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
}

void task8() {
	glTranslatef(0, baseRadius, 0);
	glPushMatrix();
	glRotatef(left_and_right, 0, 1, 0);
	drawSnowMan();
	glPopMatrix();
	glTranslatef(baseRadius + baseRadius * childScale, -baseRadius + baseRadius * childScale, 0);
	glScalef(childScale, childScale, childScale);
	glPushMatrix();
	glRotatef(left_and_right, 0, 1, 0);
	drawSnowMan();
	glPopMatrix();
	glTranslatef(baseRadius + baseRadius * childScale, -baseRadius + baseRadius * childScale, 0);
	glRotatef(left_and_right, 0, 1, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
}

void task9() {
	glTranslatef(baseRadius + baseRadius * childScale * 2 + baseRadius * childScale * childScale, 0, 0);
	glRotatef(left_and_right, 0, 1, 0);
	glTranslatef(-(baseRadius + baseRadius * childScale * 2 + baseRadius * childScale * childScale), 0, 0);
	glTranslatef(0, baseRadius, 0);
	drawSnowMan();
	glTranslatef(baseRadius + baseRadius * childScale, -baseRadius + baseRadius * childScale, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
	glTranslatef(baseRadius + baseRadius * childScale, -baseRadius + baseRadius * childScale, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
}

void task10() {
	Axes();

	// тело снеговика
	glColor3f(1, 1, 1);
	glPushMatrix();
	glutSolidSphere(baseRadius, 20, 20);

	//Вращение
	glRotatef(left_and_right, 0, 0, 1);
	glTranslatef(0, baseRadius + baseRadius * headCoefficient, 0);
	glRotatef(-left_and_right, 0, 0, 1);

	// голова снеговика
	glPushMatrix();
	glScalef(headCoefficient, headCoefficient, headCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	// глаза
	glColor3f(0, 0, 0);
	glPushMatrix();
	glRotatef(30, 0, 1, 0);
	glTranslatef(0, baseRadius * eyeCoefficient, baseRadius * headCoefficient);
	glScalef(eyeCoefficient, eyeCoefficient, eyeCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	glPushMatrix();
	glRotatef(-30, 0, 1, 0);
	glTranslatef(0, baseRadius * eyeCoefficient, baseRadius * headCoefficient);
	glScalef(eyeCoefficient, eyeCoefficient, eyeCoefficient);
	glutSolidSphere(baseRadius, 20, 20);
	glPopMatrix();
	// нос
	glColor3f(1, 0.4, 0);
	glTranslatef(0, -baseRadius * eyeCoefficient * 0.5, baseRadius * headCoefficient);
	glutSolidCone(carrotRadius, carrotHeight, 20, 20);
	glPopMatrix();
}

void task11() {
	drawSnowMan();
	glRotatef(left_and_right, 0, 1, 0);
	glTranslatef(baseRadius, 0, 0);
	glScalef(childScale, childScale, childScale);
	glTranslatef(baseRadius * 1.5, 0, 0);
	drawSnowMan();
	glPushMatrix();
	glRotatef(left_and_right, 0, 0, 1);
	glTranslatef(0, baseRadius * 2 + baseRadius * childScale, 0);
	glScalef(childScale, childScale, childScale);
	drawSnowMan();
	glPopMatrix();
	glTranslatef(0, baseRadius + baseRadius * headCoefficient, 0);
	glRotatef(left_and_right, 0, 1, 0);
	glTranslatef(baseRadius * headCoefficient * 6, 0, 0);
	glScalef(childScale * childScale, childScale * childScale, childScale * childScale);
	drawSnowMan();
}

void task12() {
	drawSnowMan();
	glPushMatrix();
	glRotatef(left_and_right, 0, 0, 1);
	glTranslatef(baseRadius + baseRadius * headCoefficient * 2 + baseRadius * childScale * childScale, 0, 0);
	glRotatef(-left_and_right, 0, 0, 1);
	glScalef(childScale * childScale, childScale * childScale, childScale * childScale);
	drawSnowMan();
	glPopMatrix();
	glColor3f(0.7, 0.0, 1.0);
	glTranslatef(0, baseRadius + baseRadius * headCoefficient * 2, 0);
	if (left_and_right > 0 && left_and_right < 180) {
		float childbody = baseRadius * childScale * childScale * 2;
		float childhead = baseRadius * childScale * childScale * 2 * headCoefficient;
		float radians = 2 * 3.14 * left_and_right / 360.0;
		glTranslatef(0, (childbody + childhead) * sin(radians), 0);
		glTranslatef(0, 0.1, 0);
		glRotatef(2 * left_and_right, 0, 0, 1);
		glTranslatef(0, -0.1, 0);
	}

	glRotatef(-90, 1, 0, 0);
	glutSolidCone(baseRadius * headCoefficient * 0.5, 0.2, 20, 20);
}

void scene(int task) {
	switch (task) {
	case(1):
		task1();
		break;
	case(2):
		task2();
		break;
	case(3):
		task3();
		break;
	case(4):
		task4();
		break;
	case(5):
		task5();
		break;
	case(6):
		task6();
		break;
	case(7):
		task7();
		break;
	case(8):
		task8();
		break;
	case(9):
		task9();
		break;
	case(10):
		task10();
		break;
	case(11):
		task11();
		break;
	case(12):
		task12();
		break;
	default:
		break;
	}
}

void Display() {
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glViewport(0, 0, 600, 600);
	glLoadIdentity();
	Axes();
	scene(task);

	glViewport(600, 0, 600, 600);
	glLoadIdentity();
	glRotatef(90, 1, 0, 0);
	Axes();
	scene(task);
	glutSwapBuffers();
}

void Initialize() {
	glClearColor(0.3, 0.3, 0.3, 1.0);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(-2, 2, -2, 2, -2.0, 2.0);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	glEnable(GL_DEPTH_TEST);
}

int main(int argc, char** argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB);
	glutInitWindowSize(1200, 800);
	glutInitWindowPosition(10, 20);
	glutCreateWindow("Компьютерная графика 2 лаба");
	glutDisplayFunc(Display);
	glutSpecialFunc(specialkeys);
	Initialize();
	glutMainLoop();
	return 0;
}