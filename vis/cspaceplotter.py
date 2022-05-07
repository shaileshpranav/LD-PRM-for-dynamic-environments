from pydoc import visiblename
import numpy as np
import matplotlib.pyplot as plt
from src.configurationspace import ConfigurationSpace
from src.robot import TurtleBot
import params.constants as CONST
import src.obstructioncheck as oc
from math import cos, sin

class CSpacePlotter:
    def __init__(self, c_space):
        self.c_space = c_space
        self.obstacle_patches = []

    def plotMap(self, fig, ax):
        height = self.c_space.height
        width = self.c_space.width
        padding =  self.c_space.padding

        sq1_pts = self.c_space.coord_sq1
        sq2_pts = self.c_space.coord_sq2
        sq3_pts = self.c_space.coord_sq3
        circle1 = self.c_space.circle1
        circle2 = self.c_space.circle2
        circle3 = self.c_space.circle3
        circle4 = self.c_space.circle4

        border_left_pts = self.c_space.boundary_left
        border_right_pts = self.c_space.boundary_right
        border_up_pts = self.c_space.boundary_up
        border_down_pts = self.c_space.boundary_down

        


        #poly_pts = self.c_space.coord_poly
        #rect_pts = self.c_space.coord_rect
        #rhom_pts = self.c_space.coord_rhom
        #circle = self.c_space.circle
        #ellipse = self.c_space.ellipse
        
        #fig = plt.figure()
        fig.set_dpi(100)
        fig.set_size_inches(8.5,6)
        #ax = plt.axes(xlim=(0,width),ylim=(0,height))
        cir1 = plt.Circle((circle1[1]), circle1[0], fc=None)
        cir2 = plt.Circle((circle2[1]) ,circle2[0], fc=None)
        cir3 = plt.Circle((circle3[1]), circle3[0], fc=None)
        cir4 = plt.Circle((circle4[1]), circle4[0], fc=None)

        
        sq1 = plt.Polygon(sq1_pts)
        sq2 = plt.Polygon(sq2_pts)
        sq3 = plt.Polygon(sq3_pts)
        border_left = plt.Polygon(border_left_pts, fc='black')
        border_right = plt.Polygon(border_right_pts,fc='black')
        border_up = plt.Polygon(border_up_pts,fc='black')
        border_down = plt.Polygon(border_down_pts,fc='black')
        borders = plt.Rectangle((-5,-5), width, height, alpha=1, fill=None, ec='b', linewidth=padding)

        self.reset(ax)        

        # shapes = [cir1, cir2, cir3, cir4, sq1, sq2, sq3, border_left, border_right, border_up, border_down]
        shapes = [border_left, border_right, border_up, border_down]
        for shape in shapes:
            plt.gca().add_patch(shape)
            ax.add_patch(shape)

        ax.set_facecolor((0.4, 0.4, 0.4))
        self.plot_prm_graph(ax)

        self.plot_cspace_obstacles(ax)
        return fig
    
    def transform_pts(self,pts,theta):
        pts= ( np.dot(np.array([ [cos(theta), -sin(theta)], [sin(theta), cos(theta)]]) , pts.T) ).T
        return pts

    def plot_prm_graph(self, ax, color=CONST.GRAPH_CLR):
        c_space_graph = self.c_space.graph
        num_edges = 0
        for parent, children in c_space_graph.items():
            #children = c_space_graph.get(tuple(node))
            for child in children:
                if not self.is_edge_intersecting(parent, child, self.c_space.obstacle_list):
                    ax.plot([parent[0], child[0]], [parent[1], child[1]], color=(0.8,0.8,0.8,0.2),linewidth=3)
                ax.scatter(child[0], child[1], alpha=0.8, c='w', edgecolors='none', s=30)
                num_edges += 1
        print('num_edges', num_edges)

    def plot_cspace_obstacles(self, ax):
        # print("Obstacle list: ",self.c_space.obstacle_list)
        self.reset_obstacle_patches()
        for obstacle in self.c_space.obstacle_list:
            w_l = 0.5
            pts = np.array([
                [0+obstacle[0], 0-w_l*obstacle[0]],
                [0+obstacle[0], 0+w_l*obstacle[0]],
                [0-obstacle[0], 0+w_l*obstacle[0]],
                [0-obstacle[0], 0-w_l*obstacle[0]],
                [0+obstacle[0], 0-w_l*obstacle[0]],
                ])
            # pts = np.vstack((pts,pts[0]))
            pts = self.transform_pts(pts,1.5)
            pts[:,0]+=obstacle[1][0]
            pts[:,1]+=obstacle[1][1]
            cir = plt.Polygon(pts, fc='red', ec='black', closed=True)
            # cir = plt.Circle((obstacle[1]), obstacle[0], fc=None)
            # plt.gca().add_patch(cir)
            self.obstacle_patches.append(ax.add_patch(cir))

    def reset_obstacle_patches(self):
        # print(f"length = {len(self.obstacle_patches)}")
        for i in reversed(range(len(self.obstacle_patches))):
            # print (f"Obs paths:{i},,,,{self.obstacle_patches[i]}")
            self.obstacle_patches[i].remove()
            self.obstacle_patches.pop()

    def reset(self,ax):
    #    for i in range(len(self.sq1)):
    #         self.sq1[i].remove()
    #         self.sq1.pop()
        [p.remove() for p in reversed(ax.patches)]

    def is_edge_intersecting(self, p1, p2, obstacle_list):
        for obstacle in obstacle_list:
            if oc.is_line_circle_intersecting(p1, p2, obstacle[1], obstacle[0]):
                return True
        return False
    
        




if __name__ == "__main__":
    t_bot = TurtleBot(radius=(0.105), clearance=0.4, wheel_rad=(0.033), dist_bet_wheels=0.16)
    c_space = ConfigurationSpace(x_limit=(-5, 5), y_limit=(-5,5), radius_of_bot=t_bot.radius, clearance=0.45)
    plotter = CSpacePlotter(c_space)

    fig, ax = plt.subplots()
    plt.xlim(c_space.x_limit[0]-0.1, c_space.x_limit[1]+0.1)
    plt.ylim(c_space.y_limit[0]-0.1, c_space.y_limit[1]+0.1)
    plt.grid(visible=False)
    ax.set_aspect('equal')

    plotter.plotMap(fig, ax)
    plt.savefig("c_space.png")

    fig.show()
    plt.draw()
    plt.show()
