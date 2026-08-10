#include <stdio.h>

typedef struct {
    int x;
    int y;
} Point;

typedef struct {
    Point top_left;
    int width;
    int height;
} Rectangle;

int rectangle_area(const Rectangle *r) {
    return r->width * r->height;
}

void print_point(Point p) {
    printf("(%d, %d)\n", p.x, p.y);
}

int main(void) {
    Point p1 = {1, 2};
    print_point(p1);

    Rectangle rect = {.top_left = {0, 0}, .width = 10, .height = 5};
    printf("rectangle top-left: ");
    print_point(rect.top_left);
    printf("rectangle area: %d\n", rectangle_area(&rect));

    /* array of structs */
    Point points[3] = {{0, 0}, {1, 1}, {2, 4}};
    for (int i = 0; i < 3; i++) {
        print_point(points[i]);
    }

    return 0;
}
