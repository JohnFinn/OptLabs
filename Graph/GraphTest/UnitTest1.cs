using System.Collections.Generic;
using System.Linq;
using Graph;
using Xunit;

namespace GraphTest
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            var g = new Graph<int> {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
            g.Connect(1,4,7);
            g.Connect(1,3,2);
            g.Connect(1,2,5);
            g.Connect(2,5,6);
            g.Connect(3,5,5);
            g.Connect(3,6,7);
            g.Connect(4,6,4);
            g.Connect(5,8,2);
            g.Connect(5,9,8);
            g.Connect(6,7,9);
            g.Connect(6,8,5);
            g.Connect(7,10,4);
            g.Connect(8,10,9);
            g.Connect(9,10,7);
            Assert.Equal(8u, g.Path(5,9));
            
            
            Assert.Equal(7u, g.Path(1,4));
            Assert.Equal(2u, g.Path(1,3));
            Assert.Equal(5u, g.Path(1,2));
            
            Assert.Equal(9u, g.Path(1,6));
            Assert.Equal(7u, g.Path(1,5));

            Assert.Equal(18u, g.Path(1,7));
            Assert.Equal(9u, g.Path(1,8));
            Assert.Equal(15u, g.Path(1,9));

            Assert.Equal(18u, g.Path(1,10));
        }
    }
}
