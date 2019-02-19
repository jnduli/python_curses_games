class Collision():
    def check_for_collisions(self, hero, villains):
        hero_points = hero.bounding_box()
        for v in villains:
            for point in hero_points:
                if v.is_point_in_car(point):
                    return True
        return False
