from hypothesis import given
import hypothesis.strategies as st
from convexhull import * 
'''
generates a random list of coordinates in the range (0,0) to (1000000,1000000)
where each list has at least three points,
and prohibiting duplicates.
one weakness: this is unlikely to generate collinear points
(it is possible but improbable), so
a test that includes collinear points might also be useful
'''

def checkHull(hull, points):
	for i in range(0, len(hull) - 2):
		j = i + 1
		p = hull[i]
		q = hull[j]
		pos = 0
		neg = 0
		for r in points:
			if r==p or r == q: continue
			if cw(p,q,r):
				neg += 1
			elif ccw(p,q,r):
				pos += 1
		if (pos == 0 or neg == 0):
			return True
		else:
			return False

@given(
    st.lists(
        st.tuples(
            st.integers(0, 10),
            st.integers(0, 10)
        ),
        min_size=10,
        max_size=20,
        unique_by=None,
        unique=True,
    )
)
def test_hull(points):
    hull = computeHull(points)
    assert checkHull(hull, points)

if __name__ == "__main__":
	test_hull()
